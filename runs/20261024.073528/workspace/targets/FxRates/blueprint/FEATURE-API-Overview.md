# FEATURE: API Overview

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Serves health, rate database summary, available currencies, and API reference documentation. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /health, GET /stats, GET /currencies, GET /docs |
| Consumes    | rates.list |

## Purpose

Expose service health, a summary of persisted rate history, the currencies present in storage, and FastAPI's API reference entry point. All values are derived from repository queries.

## Routes

### GET /health

Returns status 200 and JSON `{"status": "ok"}`.

### GET /stats

Returns status 200 with `dates`, `rates`, `first`, and `last`. `dates` counts distinct dates with stored rates; `rates` counts stored rows. `first` and `last` are the earliest and latest dates, or null when no rows exist.

### GET /currencies

Returns status 200 with base `EUR` and every currency with at least one stored rate, sorted ascending. EUR is the implicit base currency and need not appear in the stored list.

### GET /docs

Returns the FastAPI API reference entry point.

## Database Interface


- None — persistence is owned by FEATURE-CLI.md, FEATURE-Rate-Loading.md.

## Programmatic Acceptance

=== AC overview-health ===
Intent: The health route returns a successful JSON response.
Requires: python-package=httpx; scope=test

from app_server.testing import web_client

response = web_client().get("/health")
assert response.status_code == 200
assert response.json()["status"] == "ok"
=== END AC overview-health ===

=== AC overview-stats ===
Intent: Statistics are computed from persisted rows, including their distinct dates.
Requires: python-package=httpx; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    date = "2099-01-07"
    currency = "QAZ"
    rate = "1.2"
    db.rates.upsert(date=date, currency=currency, rate=rate)

body = web_client().get("/stats").json()
assert body["dates"] >= 1
assert body["rates"] >= 1
assert body["first"] is not None
assert body["last"] is not None
=== END AC overview-stats ===

=== AC overview-currencies ===
Intent: The currency route lists a currency that has a persisted rate.
Requires: python-package=httpx; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    date = "2099-01-08"
    currency = "QAZ"
    rate = "1.2"
    db.rates.upsert(date=date, currency=currency, rate=rate)

body = web_client().get("/currencies").json()
assert body["base"] == "EUR"
assert currency in body["currencies"]
=== END AC overview-currencies ===

=== AC overview-docs ===
Intent: FastAPI exposes its programmatic API reference entry point.
Requires: python-package=httpx; scope=test

from app_server.testing import web_client

response = web_client().get("/docs")
assert response.status_code == 200
assert response.headers["content-type"].startswith("text/html")
=== END AC overview-docs ===

## User Acceptance

- None.

## Guardrails

- Derive summary counts, date bounds, and currencies from persisted rates.
- Keep currencies sorted ascending.
- Preserve the API reference entry point.
