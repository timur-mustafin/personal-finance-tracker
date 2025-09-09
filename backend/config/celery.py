
import os
from celery import Celery
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")
app = Celery("backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Beat schedule: nightly FX sync at 02:00 UTC
app.conf.beat_schedule = {
    "sync-fx-nightly": {
        "task": "backend.core.tasks.sync_rates_task",
        "schedule": timedelta(hours=24),
        "options": {"expires": 3600},
    }
}
