
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Currency
from transactions.models import TransactionCategory

class Command(BaseCommand):
    help = "Seed basic currencies and default categories."

    @transaction.atomic
    def handle(self, *args, **options):
        currencies = [("USD","US Dollar"),("EUR","Euro"),("RSD","Serbian Dinar")]
        for code, name in currencies:
            Currency.objects.get_or_create(code=code, defaults={"name": name})

        defaults = [("Income", True),("Groceries", False),("Transport", False),("Rent", False),
                    ("Utilities", False),("Entertainment", False),("Healthcare", False)]
        for title, is_income in defaults:
            TransactionCategory.objects.get_or_create(name=title, defaults={"is_income": is_income, "color": "#9CA3AF"})

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
