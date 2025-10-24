
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import random
import datetime

from core.models import Currency, TransactionCategory, Budget
from transactions.models import Transaction  # <- Transaction lives in the transactions app

class Command(BaseCommand):
    help = "Seed demo data: currencies, categories, budgets, and random transactions"

    def add_arguments(self, parser):
        parser.add_argument("--user", default="admin", help="Username to own the demo data")
        parser.add_argument("--months", type=int, default=3, help="How many past months to generate")
        parser.add_argument("--tx-per-month", type=int, default=60, help="Approximate transactions per month")

    def handle(self, *args, **opts):
        User = get_user_model()
        username = opts["user"]
        months = opts["months"]
        tx_per_month = opts["tx_per_month"]

        user, _ = User.objects.get_or_create(username=username, defaults={"email": f"{username}@example.com"})
        if not user.password:
            user.set_password("admin")
            user.save(update_fields=["password"])

        # Ensure basic seed exists (currencies & categories)
        currencies = [
            ("USD", "US Dollar", "$"),
            ("EUR", "Euro", "€"),
            ("RSD", "Serbian Dinar", "RSD"),
        ]
        currency_map = {}
        for code, name, sym in currencies:
            c, _ = Currency.objects.get_or_create(code=code, defaults={"name": name, "symbol": sym})
            currency_map[code] = c

        income_names = ["Salary", "Bonus", "Gift", "Interest"]
        expense_names = ["Groceries", "Rent", "Utilities", "Transport", "Dining", "Health", "Entertainment", "Shopping"]
        income = [TransactionCategory.objects.get_or_create(name=n, defaults={"is_income": True})[0] for n in income_names]
        expense = [TransactionCategory.objects.get_or_create(name=n, defaults={"is_income": False})[0] for n in expense_names]

        # Prepare months list (first day of each month, including this one, going back N-1 months)
        today = timezone.now().date()
        first_of_this_month = today.replace(day=1)
        months_list = []
        cur = first_of_this_month
        for _ in range(months):
            months_list.append(cur)
            # move to previous month first day
            prev = (cur - datetime.timedelta(days=1)).replace(day=1)
            cur = prev

        # Budgets for expense categories for each month
        for m in months_list:
            for cat in expense:
                limit = random.randint(150, 900) * 1.0
                Budget.objects.get_or_create(user=user, category=cat, month=m, defaults={"limit_amount": Decimal(f"{limit:.2f}")})

        # Fresh transactions for the user (keep budgets)
        Transaction.objects.filter(user=user).delete()

        rng = random.Random(42)
        def rand_date_in_month(month_date):
            # month_date is first day of month
            if month_date.month == 12:
                next_month = datetime.date(month_date.year + 1, 1, 1)
            else:
                next_month = datetime.date(month_date.year, month_date.month + 1, 1)
            delta_days = (next_month - month_date).days
            return month_date + datetime.timedelta(days=rng.randrange(delta_days))

        for m in months_list:
            # Incomes: 1-2 per month
            for _ in range(rng.randint(1, 2)):
                Transaction.objects.create(
                    user=user,
                    category=rng.choice(income),
                    currency=currency_map["EUR"],
                    amount=Decimal(f"{rng.randrange(1200, 2600)}.00"),
                    description="Monthly income",
                    date=rand_date_in_month(m),
                )

            # Expenses
            n = int(rng.normalvariate(tx_per_month, max(1, int(tx_per_month*0.2))))
            n = max(20, min(3 * tx_per_month, n))
            for _ in range(n):
                cat = rng.choice(expense)
                base = {
                    "Groceries": (5, 80),
                    "Rent": (400, 800),
                    "Utilities": (20, 150),
                    "Transport": (3, 40),
                    "Dining": (8, 60),
                    "Health": (10, 120),
                    "Entertainment": (5, 70),
                    "Shopping": (10, 200),
                }.get(cat.name, (5, 100))
                amount = rng.uniform(*base)
                curr = rng.choice([currency_map["EUR"], currency_map.get("RSD") or currency_map["EUR"], currency_map["USD"]])
                Transaction.objects.create(
                    user=user,
                    category=cat,
                    currency=curr,
                    amount=Decimal(f"{amount:.2f}"),
                    description=f"{cat.name} expense",
                    date=rand_date_in_month(m),
                )

        self.stdout.write(self.style.SUCCESS(f"Seeded demo data for user '{username}' across {months} months."))


from django.utils import timezone
from decimal import Decimal
from core.models import Currency
from transactions.models import Transaction, TransactionCategory

def create_initial_balances(user):
    income_cat, _ = TransactionCategory.objects.get_or_create(name="Initial Balance", is_income=True, defaults={'color':'#10B981'})
    usd = Currency.objects.get(code="USD")
    eur = Currency.objects.get(code="EUR")
    rsd = Currency.objects.get(code="RSD")
    today = timezone.now().date()
    Transaction.objects.get_or_create(user=user, category=income_cat, currency=usd, amount=Decimal('1500.00'), description="Seed USD balance", date=today)
    Transaction.objects.get_or_create(user=user, category=income_cat, currency=eur, amount=Decimal('800.00'), description="Seed EUR balance", date=today)
    Transaction.objects.get_or_create(user=user, category=income_cat, currency=rsd, amount=Decimal('120000.00'), description="Seed RSD balance", date=today)
