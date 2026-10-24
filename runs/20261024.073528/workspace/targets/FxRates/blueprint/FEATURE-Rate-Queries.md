# FEATURE: Rate Queries

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Retrieves ECB rates for a requested date or the latest publication. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /rates/{date}, GET /rates/latest |
| Consumes    | rates.list |

## Purpose

Return the stored rates for the latest publication date on or before the requested date. The API uses the same effective-date rule for date requests and the latest publication for `/rates/latest`.

## Routes

| Method | Path | Behavior |
|--------|------|----------|
| GET | `/rates/{date}` | Resolve the supplied calendar date to the latest publication on or before it. |
| GET | `/rates/latest` | Return the rates for the latest publication, with `"requested": "latest"`. |

A successful response is `{"date": <effective date>, "requested": <requested date or "latest">, "base": "EUR", "rates": {<currency>: <stored rate text>, ...}}`. Include every stored currency rate on the effective publication date. Return 404 when no publication exists on or before the requested date. A malformed or impossible calendar date returns 422.

## Database Interface


- None — persistence is owned by FEATURE-CLI.md, FEATURE-Rate-Loading.md.

## Programmatic Acceptance

=== AC effective-date ===
Intent: A date request resolves to a stored publication on or before the requested date.

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    date = "2099-01-02"
    currency = "QAZ"
    rate = "1.234"
    db.rates.upsert(date=date, currency=currency, rate=rate)

client = web_client()
response = client.get(f"/rates/{date}")
assert response.status_code == 200
body = response.json()
assert body["date"] == date
assert body["requested"] == date
assert body["base"] == "EUR"
assert body["rates"][currency] == rate
=== END AC effective-date ===

=== AC no-effective-date ===
Intent: A request before every stored publication returns the documented not-found status.

from app_server.testing import web_client

client = web_client()
response = client.get("/rates/1900-01-01")
assert response.status_code == 404
=== END AC no-effective-date ===

=== AC latest-rates ===
Intent: The latest endpoint returns the latest publication and its stored rates.

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    date = "2099-01-03"
    currency = "QAZ"
    rate = "1.234"
    db.rates.upsert(date=date, currency=currency, rate=rate)

client = web_client()
response = client.get("/rates/latest")
assert response.status_code == 200
body = response.json()
assert body["date"] == date
assert body["requested"] == "latest"
assert body["base"] == "EUR"
assert body["rates"][currency] == rate
=== END AC latest-rates ===

=== AC malformed-date ===
Intent: A malformed or impossible date is rejected with the documented validation status.

from app_server.testing import web_client

client = web_client()
response = client.get("/rates/2025-13-01")
assert response.status_code == 422
=== END AC malformed-date ===

## User Acceptance

- None.

## Guardrails

- Rates come from persisted rows through the declared repository operation.
- Preserve published rate strings in responses.
- Resolve dates using the latest available publication on or before the requested date.
