from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
from django.db import transaction as db_transaction
from django.utils.dateparse import parse_date
from core.models import Currency, TransactionCategory
import csv, io

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='export')
    def export_csv(self, request):
        # Export current user's transactions as CSV content string
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["date", "amount", "currency", "category", "description"])
        qs = self.get_queryset().select_related("currency", "category").order_by("date")
        for t in qs:
            writer.writerow([
                t.date.isoformat(),
                str(t.amount),
                t.currency.code if t.currency else "",
                t.category.name if t.category else "",
                t.description or ""
            ])
        output.seek(0)
        return Response({"filename": "transactions.csv", "content": output.getvalue()})

    @action(detail=False, methods=['post'], url_path='import')
    def import_csv(self, request):
        """Accepts CSV file (columns: date, amount, currency, category, description)
        Returns JSON report with created count and per-line errors.
        """
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided under 'file'."}, status=status.HTTP_400_BAD_REQUEST)

        decoded = file.read().decode('utf-8', errors='ignore')
        reader = csv.DictReader(io.StringIO(decoded))
        required = {"date", "amount"}
        report = {"created": 0, "errors": 0, "line_errors": []}

        with db_transaction.atomic():
            for i, row in enumerate(reader, start=2):  # header is line 1
                # Validate required columns
                missing = [k for k in required if not (row.get(k) or "").strip()]
                if missing:
                    report["errors"] += 1
                    report["line_errors"].append({"line": i, "error": f"Missing required: {', '.join(missing)}"})
                    continue

                d = parse_date((row.get("date") or "").strip())
                if not d:
                    report["errors"] += 1
                    report["line_errors"].append({"line": i, "error": "Invalid date"})
                    continue

                try:
                    amt = float((row.get("amount") or "0").strip())
                except Exception:
                    report["errors"] += 1
                    report["line_errors"].append({"line": i, "error": "Invalid amount"})
                    continue

                currency = None
                code = (row.get("currency") or "").strip().upper()
                if code:
                    currency, _ = Currency.objects.get_or_create(code=code, defaults={"name": code})

                category = None
                cname = (row.get("category") or "").strip()
                if cname:
                    category, _ = TransactionCategory.objects.get_or_create(name=cname)

                Transaction.objects.create(
                    user=request.user,
                    amount=amt,
                    currency=currency,
                    category=category,
                    description=(row.get("description") or "").strip(),
                    date=d
                )
                report["created"] += 1

        return Response(report, status=status.HTTP_201_CREATED)
