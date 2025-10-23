from django.core.management.base import BaseCommand, CommandParser
from datetime import date, timedelta
from core.models import Currency, ExchangeRate

class Command(BaseCommand):
    help = "Seed demo USD/EUR/RSD exchange rates."

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("--days", type=int, default=7)
        parser.add_argument("--usd-eur", type=float, default=0.92)
        parser.add_argument("--usd-rsd", type=float, default=108.5)

    def handle(self, *args, **opts):
        days = opts["days"]
        usd_eur = opts["usd_eur"]
        usd_rsd = opts["usd_rsd"]
        for code in ("USD","EUR","RSD"):
            Currency.objects.get_or_create(code=code, defaults={"name": code})
        today = date.today()
        for i in range(days):
            d = today - timedelta(days=i)
            ExchangeRate.objects.update_or_create(base="USD", target="EUR", date=d, defaults={"rate": usd_eur})
            ExchangeRate.objects.update_or_create(base="EUR", target="USD", date=d, defaults={"rate": 1.0/usd_eur})
            ExchangeRate.objects.update_or_create(base="USD", target="RSD", date=d, defaults={"rate": usd_rsd})
            ExchangeRate.objects.update_or_create(base="RSD", target="USD", date=d, defaults={"rate": 1.0/usd_rsd})
            # Derived cross-rates for convenience
            eur_rsd = usd_rsd / usd_eur if usd_eur else None
            rsd_eur = usd_eur / usd_rsd if usd_rsd else None
            if eur_rsd:
                ExchangeRate.objects.update_or_create(base="EUR", target="RSD", date=d, defaults={"rate": eur_rsd})
            if rsd_eur:
                ExchangeRate.objects.update_or_create(base="RSD", target="EUR", date=d, defaults={"rate": rsd_eur})
        self.stdout.write(self.style.SUCCESS(f"Seeded FX for {days} day(s)."))
