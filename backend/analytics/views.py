from datetime import date
from collections import defaultdict
from django.conf import settings
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from transactions.models import Transaction
from core.models import ExchangeRate, Budget, TransactionCategory

def _rate_on_or_before(base: str, target: str, on_date):
    return (ExchangeRate.objects
            .filter(base=base, target=target, date__lte=on_date)
            .order_by('-date')
            .first())

def convert_amount(amount, src: str, tgt: str, on_date):
    if src == tgt:
        return float(amount)
    base = getattr(settings, 'BASE_CURRENCY', 'USD')
    if src == base:
        in_base = float(amount)
    else:
        r = _rate_on_or_before(base, src, on_date)
        in_base = float(amount) if not r or float(r.rate) == 0.0 else float(amount) / float(r.rate)
    if tgt == base:
        return in_base
    r2 = _rate_on_or_before(base, tgt, on_date)
    return in_base if not r2 else in_base * float(r2.rate)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def summary_by_month(request):
    target_currency = request.query_params.get('currency', getattr(settings, 'BASE_CURRENCY', 'USD'))
    qs = (Transaction.objects
          .filter(user=request.user)
          .annotate(month=TruncMonth('date'))
          .values('month','currency__code','category__is_income')
          .annotate(total=Sum('amount'))
          .order_by('month'))
    buckets = defaultdict(lambda: {'income': 0.0, 'expense': 0.0})
    for row in qs:
        code = row['currency__code'] or getattr(settings, 'BASE_CURRENCY', 'USD')
        val = convert_amount(row['total'], code, target_currency, row['month'] or date.today())
        key = 'income' if row['category__is_income'] else 'expense'
        buckets[row['month'].strftime('%Y-%m') if row['month'] else 'unknown'][key] += float(val)
    out = [{'month': m, **vals, 'net': vals['income'] - vals['expense']} for m, vals in sorted(buckets.items())]
    return Response(out)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_categories(request):
    target_currency = request.query_params.get('currency', getattr(settings, 'BASE_CURRENCY', 'USD'))
    limit = int(request.query_params.get('limit', '5'))
    qs = (Transaction.objects
          .filter(user=request.user, category__is_income=False)
          .values('category__name','currency__code','date')
          .annotate(total=Sum('amount'))
          .order_by('-total'))
    agg = defaultdict(float)
    for row in qs:
        code = row['currency__code'] or getattr(settings, 'BASE_CURRENCY', 'USD')
        val = convert_amount(row['total'], code, target_currency, row['date'] or date.today())
        agg[row['category__name'] or 'Uncategorized'] += float(val)
    items = sorted(agg.items(), key=lambda kv: kv[1], reverse=True)[:limit]
    return Response([{'category': k, 'total': v} for k, v in items])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def budgets_summary(request):
    month = request.query_params.get('month')
    target_currency = request.query_params.get('currency', getattr(settings, 'BASE_CURRENCY', 'USD'))
    if not month:
        today = date.today()
        month = f"{today.year}-{today.month:02d}"
    m_year, m_month = map(int, month.split('-'))
    from datetime import date as _d
    first_day = _d(m_year, m_month, 1)

    tx = (Transaction.objects
          .filter(user=request.user, date__year=m_year, date__month=m_month, category__is_income=False)
          .values('category__id','category__name','currency__code','date')
          .annotate(total=Sum('amount')))

    spent = defaultdict(float)
    for row in tx:
        code = row['currency__code'] or getattr(settings, 'BASE_CURRENCY', 'USD')
        spent[row['category__id']] += convert_amount(row['total'], code, target_currency, row['date'] or first_day)

    budgets = (Budget.objects
               .filter(user=request.user, month=first_day)
               .select_related('category'))

    out = []
    for b in budgets:
        s = float(spent.get(b.category_id, 0.0))
        out.append({
            'category': b.category.name,
            'limit': float(b.limit_amount),
            'spent': s,
            'remaining': float(b.limit_amount) - s,
        })
    return Response(out)
