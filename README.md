# Personal Finance Tracker+


```bash
docker compose build frontend
docker compose up -d db redis backend worker beat frontend
```

# Apply migrations & (optionally) auto-create the superuser (your .env has admin creds)

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```
# add 3 months of data samples, ~60 tx per month, owned by 'admin'

```bash
docker compose exec backend python manage.py seed_demo --user admin --months 3 --tx-per-month 60
```

# Open the app
Start-Process with login at http://localhost:9080/login
& http://localhost:9080/ for the dashboard itself


- `worker`: processes async tasks
- `beat`: schedules the nightly `sync_rates_task`
- If you skip `worker/beat`, the app still runs; rates sync on boot only.



http://localhost:9080/login