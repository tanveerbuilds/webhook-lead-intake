#!/usr/bin/env python3
"""
Sample lead-intake webhook (demonstration only).

Receives lead payloads from chatbots/forms, validates a shared secret,
and appends them to a local JSONL file. Shows the shape of a real intake
endpoint; not hardened for production (no rate limiting, local file
storage).

Run:
    export WEBHOOK_SECRET=choose-a-long-random-string
    uvicorn app:app --port 8000

Test (in another terminal, same WEBHOOK_SECRET):
    python test_client.py
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

SECRET = os.environ.get("WEBHOOK_SECRET", "")
STORE = Path(__file__).parent / "leads.jsonl"

app = FastAPI(title="Sample lead-intake webhook")


class Lead(BaseModel):
    name: str
    email: str
    source: str = "unknown"
    notes: str = ""


@app.post("/webhook/leads")
def intake(lead: Lead, x_webhook_secret: str = Header(default="")):
    if not SECRET or x_webhook_secret != SECRET:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")
    record = {
        "received_at": datetime.now(timezone.utc).isoformat(),
        **lead.model_dump(),
    }
    with open(STORE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return {"ok": True}


@app.get("/leads")
def list_leads():
    if not STORE.exists():
        return []
    lines = STORE.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]
