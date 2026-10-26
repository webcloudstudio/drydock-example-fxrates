# FEATURE: API Reference Endpoints

| Field | Value |
|-------|-------|
| Version | 20261025 V1 |
| Description | Serve health, database statistics, and available currencies. |
| Depends On | FEATURE-ApiFoundation.md, DATABASE.md |
| Provides | GET /health, GET /stats, GET /currencies |
| Consumes | rates repository operations |

## Purpose

Provide JSON health, store statistics, and the sorted currency list from persisted rates.

## Routes

- `GET /health` returns status 200 and `{"status":"ok"}`.
- `GET /stats` returns publication-date and rate counts, plus first and last dates; both dates are null for an empty store.
- `GET /currencies` returns base EUR and every currency with a stored rate, in ascending order.

## Database Interface


- None — persistence is owned by FEATURE-InitializeRates.md, FEATURE-LoadHistory.md.

## Programmatic Acceptance

=== AC reference_routes ===
Intent: The reference endpoints respond and derive statistics and currencies from stored rates.
Requires: python-package=httpx; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

date = "2099-01-02"
currency = "ZZZ"
rate = "1.2300"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

client = web_client()
health = client.get("/health")
stats = client.get("/stats")
currencies = client.get("/currencies")

assert health.status_code == 200
assert stats.status_code == 200
assert currencies.status_code == 200
assert health.json()["status"] == "ok"
assert stats.json()["dates"] >= 1
assert stats.json()["rates"] >= 1
assert stats.json()["first"] is not None
assert stats.json()["last"] is not None
assert currency in currencies.json()["currencies"]
assert currencies.json()["base"] == "EUR"
=== END AC reference_routes ===

## User Acceptance

- None.

## Guardrails

- Counts and dates come from database queries, not constants.
- Currency codes are returned in ascending order.
- Every response is JSON.
