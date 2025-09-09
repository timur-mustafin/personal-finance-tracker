
from celery import shared_task
from django.core.management import call_command

@shared_task(bind=True, ignore_result=True)
def sync_rates_task(self):
    # Reuse the management command for single source of truth
    call_command("sync_rates")
