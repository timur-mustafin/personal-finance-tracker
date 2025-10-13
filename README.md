# Personal Finance Tracker+


```bash
docker compose build frontend
docker compose up -d db redis backend worker beat frontend
```
# Open the app
Start-Process http://localhost:9080/


- `worker`: processes async tasks
- `beat`: schedules the nightly `sync_rates_task`
- If you skip `worker/beat`, the app still runs; rates sync on boot only.
