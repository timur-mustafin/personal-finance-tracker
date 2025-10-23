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


def _get_rate(base: str, target: str, on_date):
    if base == target:
        return 1.0
    # Try direct pair first
    obj = (ExchangeRate.objects
           .filter(base=base, target=target, date__lte=on_date)
           .order_by('-date')
           .first())
    if obj:
        return obj.rate
    # Try pivot via BASE_CURRENCY (e.g., USD) if direct pair missing
    pivot = getattr(settings, 'BASE_CURRENCY', 'USD')
    if base != pivot and target != pivot:
        obj1 = (ExchangeRate.objects
                .filter(base=base, target=pivot, date__lte=on_date)
                .order_by('-date')
                .first())
        obj2 = (ExchangeRate.objects
                .filter(base=pivot, target=target, date__lte=on_date)
                .order_by('-date')
                .first())
        if obj1 and obj2:
            # Multiply to get cross rate
            try:
                return float(obj1.rate) * float(obj2.rate)
            except Exception:
                return None
    return None


def convert_amount(amount, base: str, target: str, on_date):
    try:
        amt = float(amount or 0.0)
    except Exception:
        amt = 0.0
    base = base or getattr(settings, 'BASE_CURRENCY', 'USD')
    target = target or getattr(settings, 'BASE_CURRENCY', 'USD')
    if base == target:
        return amt
    rate = _get_rate(base, target, on_date)
    if rate is None:
        return amt  # fallback: no conversion available
    return amt * float(rate)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def summary_by_month(request):
    target_currency = request.query_params.get('currency', getattr(settings, 'BASE_CURRENCY', 'USD'))
    qs = (Transaction.objects
          .filter(user=request.user)
          .annotate(month=TruncMonth('date'))
          .values('month', 'currency__code')
          .annotate(total=Sum('amount'))
          .order_by('month'))

    totals = defaultdict(float)
    for row in qs:
        month = row['month'] or date.today().replace(day=1)
        code = row['currency__code'] or getattr(settings, 'BASE_CURRENCY', 'USD')
        totals[month] += convert_amount(row['total'], code, target_currency, month)

    out = [{'month': m.strftime('%Y-%m'), 'total': float(v)} for m, v in sorted(totals.items())]
    return Response(out)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_categories(request):
    target_currency = request.query_params.get('currency', getattr(settings, 'BASE_CURRENCY', 'USD'))
    qs = (Transaction.objects
          .filter(user=request.user)
          .values('category_id', 'category__name', 'currency__code')
          .annotate(total=Sum('amount'))
          .order_by())
    # Sum per category (expenses as positive magnitude)
    buckets = defaultdict(float)
    for row in qs:
        code = row['currency__code'] or getattr(settings, 'BASE_CURRENCY', 'USD')
        val = convert_amount(row['total'], code, target_currency, date.today())
        buckets[row['category__name'] or 'Uncategorized'] += float(abs(val))
    top = sorted(buckets.items(), key=lambda x: x[1], reverse=True)[:5]
    out = [{'category': k, 'total': float(v)} for k, v in top]
    return Response(out)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def budgets_summary(request):
    # Current month budgets and their spent (converted to target currency)
    target_currency = request.query_params.get('currency', getattr(settings, 'BASE_CURRENCY', 'USD'))
    first_day = date.today().replace(day=1)

    budgets = (Budget.objects
               .filter(user=request.user, month=first_day)
               .select_related('category'))
    # Spend per category for current month
    spend = (Transaction.objects
             .filter(user=request.user, date__gte=first_day)
             .values('category_id', 'currency__code')
             .annotate(total=Sum('amount')))

    from collections import defaultdict
    spent_map = defaultdict(float)
    for row in spend:
        code = row['currency__code'] or getattr(settings, 'BASE_CURRENCY', 'USD')
        spent_map[row['category_id']] += convert_amount(row['total'], code, target_currency, first_day)

    month_label = first_day.strftime('%Y-%m')
    out = []
    for b in budgets:
        s = float(spent_map.get(b.category_id, 0.0))
        base_cur = getattr(settings, 'BASE_CURRENCY', 'USD')
        limit_raw = float(b.limit_amount)
        limit = float(convert_amount(limit_raw, base_cur, target_currency, first_day))
        progress = (s / limit) if limit > 0 else 0.0
        out.append({
            'category': b.category.name,
            'limit': limit,
            'spent': s,
            'remaining': limit - s,
            'progress': max(0.0, min(1.0, progress)),
            'month': month_label,
            'currency': target_currency,
        })
    return Response(out)
