# webhook-lead-intake

> **Sample / demo build** — a minimal lead-intake webhook: receives lead payloads from chatbots or forms, validates a shared secret, and appends them to a local file. Built for learning and demonstration, not production use.

## What this sample demonstrates

- **Webhook endpoint** — `POST /webhook/leads` accepts a JSON lead payload
- **Shared-secret auth** — requests must carry the `X-Webhook-Secret` header
- **Simple storage** — accepted leads are appended to `leads.jsonl`, one JSON object per line
- **Read-back** — `GET /leads` returns everything stored so far

## Project structure

```
.
├── app.py           # Sample FastAPI webhook (sample code)
├── test_client.py   # Sends one sample lead to the local server
└── README.md
```

## How to run the sample

```bash
pip install -r requirements.txt

export WEBHOOK_SECRET=choose-a-long-random-string
uvicorn app:app --port 8000

# in another terminal, with the same WEBHOOK_SECRET set:
python test_client.py
```

Then open http://localhost:8000/leads to see the stored lead.

## Notes

- This is a **demonstration**, not a finished product: a shared secret is not real auth, there is no rate limiting, and storage is a local file.
- In production this would verify a provider signature (e.g. WhatsApp/Stripe style HMAC), write to a database or CRM, and run behind HTTPS with rate limits.

## Tech

Python · FastAPI · uvicorn · JSONL storage
