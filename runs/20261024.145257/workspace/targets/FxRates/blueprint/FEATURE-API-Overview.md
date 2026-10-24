# FEATURE: API Overview

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Provides health, rate coverage, and available-currency endpoints. |
| Depends On  | DATABASE.md, ARCHITECTURE.md |
| Provides    | GET /health, GET /stats, GET /currencies |
| Consumes    | `FEATURE-RATE-005` rates.list_all |

## Purpose

Expose service health and a database-backed summary of stored rate coverage and currencies.

## Workflow

- `GET /health` returns a JSON object with `status` set to `ok`.
- `GET /stats` returns distinct publication-date count, stored-rate count, earliest date, and latest date. Empty stores return zero counts and `null` dates.
- `GET /currencies` returns EUR as the base and the distinct currencies with at least one stored rate, sorted ascending. EUR is implicit and is not included unless it has stored rates.

## Database Interface

- `FEATURE-RATE-005` — read: list all rates - supplies: — - returns: `date`, `currency`, `rate`

## Guardrails

- Derive counts, dates, and currencies from persisted rates on each request.
- Route access to persistence through the generated library.

## Programmatic Acceptance

=== AC health-endpoint ===
Intent: The health route returns a successful response with its declared status field.

from app_server.testing import web_client

client = web_client()
response = client.get("/health")
assert response.status_code == 200
body = response.json()
assert body["status"] == "ok"
=== END AC health-endpoint ===

=== AC stats-endpoint ===
Intent: The stats route responds and reports counts and date bounds derived from the rows arranged by this check.

from persistence.testing import db_session
from app_server.testing import web_client

with db_session() as db:
    before = db.rates.list_all()
    date = "2098-01-02"
    currency = "ZZZ"
    rate = "1.234"
    db.rates.upsert(date=date, currency=currency, rate=rate)
    response = web_client().get("/stats")
    assert response.status_code == 200
    body = response.json()
    assert body["rates"] == len(before) + 1
    assert body["dates"] == len({row.date for row in before} | {date})
    assert body["first"] == min([row.date for row in before] + [date])
    assert body["last"] == max([row.date for row in before] + [date])
=== END AC stats-endpoint ===

=== AC currencies-endpoint ===
Intent: The currencies route responds and includes the currency inserted by this check.

from persistence.testing import db_session
from app_server.testing import web_client

with db_session() as db:
    date = "2098-01-03"
    currency = "ZZZ"
    db.rates.upsert(date=date, currency=currency, rate="1.25")
    response = web_client().get("/currencies")
    assert response.status_code == 200
    body = response.json()
    assert body["base"] == "EUR"
    assert currency in body["currencies"]
    assert body["currencies"] == sorted(set(body["currencies"]))
=== END AC currencies-endpoint ===
