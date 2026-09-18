#!/usr/bin/env python3
"""
Sends one sample lead to the local webhook.
Requires WEBHOOK_SECRET to match the server's secret.
"""
import os

import requests

SECRET = os.environ.get("WEBHOOK_SECRET", "")

resp = requests.post(
    "http://localhost:8000/webhook/leads",
    headers={"X-Webhook-Secret": SECRET},
    json={
        "name": "Test Lead",
        "email": "test@example.com",
        "source": "sample-form",
        "notes": "hello from test_client.py",
    },
    timeout=10,
)
print(resp.status_code, resp.json())
