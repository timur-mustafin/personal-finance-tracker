import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import date
from backend.core.models import ExchangeRate, Currency

class Command(BaseCommand):
    help = "Sync latest FX rates from exchangerate.host for BASE_CURRENCY -> all known currencies."

    def handle(self, *args, **kwargs):
        base = getattr(settings, 'BASE_CURRENCY', 'USD').upper()
        codes = list(Currency.objects.values_list('code', flat=True))
        if not codes:
            codes = ["USD","EUR","RSD","GBP","CHF","JPY","CNY"]
        symbols = ",".join(sorted(set([c.upper() for c in codes if c.upper()!=base])))
        url = f"https://api.exchangerate.host/latest?base={base}&symbols={symbols}"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            payload = r.json()
            rates = payload.get("rates", {})
            today = date.today()
            created = 0
            for quote, rate in rates.items():
                ExchangeRate.objects.update_or_create(
                    base_code=base, quote_code=quote.upper(), date=today,
                    defaults={"rate": rate}
                )
                created += 1
            self.stdout.write(self.style.SUCCESS(f"Synced {created} rates for base={base}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Rate sync failed: {e}"))
