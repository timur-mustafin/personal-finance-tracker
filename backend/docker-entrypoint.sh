#!/usr/bin/env bash
set -e

python - <<'PYCODE'
import os, sys, time
import psycopg2
host=os.getenv("POSTGRES_HOST","db")
port=int(os.getenv("POSTGRES_PORT","5432"))
user=os.getenv("POSTGRES_USER","postgres")
pwd=os.getenv("POSTGRES_PASSWORD","postgres")
db=os.getenv("POSTGRES_DB","pft_db")
for _ in range(90):
    try:
        psycopg2.connect(host=host, port=port, user=user, password=pwd, dbname=db).close()
        sys.exit(0)
    except Exception:
        time.sleep(1)
sys.exit(1)
PYCODE

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true
python manage.py seed_basics || true
python manage.py sync_rates || true

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python - <<'PYCODE'
import os, django
from django.contrib.auth import get_user_model
os.environ.setdefault("DJANGO_SETTINGS_MODULE","backend.config.settings")
django.setup()
User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
email = os.getenv("DJANGO_SUPERUSER_EMAIL","admin@example.com")
u, created = User.objects.get_or_create(username=username, defaults={"email": email, "is_superuser": True, "is_staff": True})
if created:
    u.set_password(password)
    u.save()
    print(f"Created superuser {username}")
else:
    print(f"Superuser {username} already exists")
PYCODE
fi

exec "$@"
