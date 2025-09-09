# Personal Finance Tracker+


# One-Click Production Run

```bash
docker compose run --rm frontend-build
docker compose up -d db backend nginx
```

- Nginx serves the SPA from a named volume and proxies `/api/` to Django.
- Backend entrypoint auto-migrates, collects static, and ensures a superuser (from `.env`).


---

## Nightly FX Sync (Celery + Redis)

To enable automatic daily exchange-rate updates, start the worker and beat:

```bash
docker compose run --rm frontend-build
docker compose up -d db redis backend worker beat nginx
```

- `worker`: processes async tasks
- `beat`: schedules the nightly `sync_rates_task`
- If you skip `worker/beat`, the app still runs; rates sync on boot only.
