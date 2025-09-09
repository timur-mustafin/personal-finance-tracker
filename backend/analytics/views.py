from django.conf import settings
from ..transactions.models import Transaction, TransactionCategory
from ..core.models import ExchangeRate, Budget
from ..transactions.models import Transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from transactions.models import Transaction
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import date


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def summary_by_month(request):
    tgt = request.GET.get("currency")
    base = getattr(settings,"BASE_CURRENCY","USD").upper()
    # fetch transactions and accumulate per month with per-row conversion
    from collections import defaultdict
    rows = (Transaction.objects
            .filter(user=request.user)
            .values("amount","date","currency__code","currency_code"))
    # currency_code fallback if currency FK absent
    totals = defaultdict(float)
    for row in rows:
        on = row["date"]
        amt = row["amount"]
        txn_code = row.get("currency__code") or row.get("currency_code") or base
        val = _convert_amount_by_date(amt, txn_code, on, tgt or base)
        key = on.strftime("%Y-%m")
        totals[key] += float(val)
    data = [{"month": k, "total": round(v, 2), "currency": (tgt or base)} for k,v in sorted(totals.items())]
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])

def budgets_summary(request):
    import calendar
    from datetime import date
    tgt = request.GET.get("currency")
    base = getattr(settings,"BASE_CURRENCY","USD").upper()
    res = []
    for b in Budget.objects.filter(user=request.user).order_by("-month"):
        year = b.month.year; month = b.month.month
        last_day = calendar.monthrange(year, month)[1]
        start = date(year, month, 1)
        end = date(year, month, last_day)
        q = Transaction.objects.filter(user=request.user, date__gte=start, date__lte=end)
        if b.category_id:
            q = q.filter(category_id=b.category_id)
        spent = 0.0
        for r in q.values("amount","date","currency__code","currency_code"):
            txn_code = r.get("currency__code") or r.get("currency_code") or base
            spent += _convert_amount_by_date(r["amount"], txn_code, r["date"], tgt or base)
        limit_conv = _convert_amount_by_date(b.amount_limit, base, end, tgt or base)
        progress = float(spent) / float(limit_conv) if float(limit_conv) > 0 else 0.0
        res.append({
            "id": b.id,
            "month": b.month.strftime("%Y-%m"),
            "category": getattr(b.category, "title", "All categories"),
            "limit": round(float(limit_conv), 2),
            "spent": round(float(spent), 2),
            "progress": round(progress, 4),
            "currency": tgt or base
        })
    return Response(res)


from datetime import date

def _get_rate_on_or_before(base_code, quote_code, on_date):
    qs = (ExchangeRate.objects
          .filter(base_code=base_code.upper(), quote_code=quote_code.upper(), date__lte=on_date)
          .order_by("-date"))
    return qs.first()

def _convert_amount_by_date(amount, txn_code, on_date, target_code):
    """Convert amount from txn_code to target_code using historical rates.
    We only store rates for BASE->other. So:
      - If txn_code == BASE and target == BASE: return amount
      - txn->BASE: divide by rate(BASE->txn) on/on_before date
      - BASE->target: multiply by rate(BASE->target) on/on_before date
    If missing rate(s), fall back to passthrough.
    """
    base = getattr(settings, "BASE_CURRENCY", "USD").upper()
    amt = float(amount or 0)
    src = (txn_code or base).upper()
    tgt = (target_code or base).upper()

    # No-op cases
    if src == tgt:
        return amt

    # First: get amount in BASE
    if src == base:
        in_base = amt
    else:
        r = _get_rate_on_or_before(base, src, on_date)
        if not r or float(r.rate) == 0.0:
            in_base = amt  # fallback
        else:
            in_base = amt / float(r.rate)

    # Then: BASE -> target
    if tgt == base:
        return in_base
    r2 = _get_rate_on_or_before(base, tgt, on_date)
    if not r2:
        return in_base  # fallback
    return in_base * float(r2.rate)

