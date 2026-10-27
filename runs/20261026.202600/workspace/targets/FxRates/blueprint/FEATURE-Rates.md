# FEATURE: Effective-Date Rates

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Retrieves stored rates for the latest publication on or before a requested date. |
| Depends On  | FEATURE-AppServer.md, DATABASE.md |
| Provides    | GET /rates/{date} |
| Consumes    | create_app(), rates repository operations |

## Purpose

Return the ECB rates for a requested date using the latest available publication on or before that date.

## Trigger and workflow

A caller requests `GET /rates/{date}`. Validate that the path value is a real calendar date in `YYYY-MM-DD` form. Find the latest publication on or before the request, then return its stored rates as published text.

Return `404` when no publication exists on or before the requested date. Malformed dates return `422`.

## Database Interface

- `FEATURE-RATE-003` — read: find publications on or before a date - supplies: `requested_date` - returns: `date`, `currency`, `rate`
- `FEATURE-RATE-002` — read: list rates for a publication date - supplies: `date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC rates-effective-date ===
Intent: The route resolves a requested date to the latest available publication and returns its stored rates.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

requested = "2099-06-03"
effective = "2099-06-02"
currency = "QAF"
rate = "6.125"

with db_session() as db:
    db.rates.upsert(date=effective, currency=currency, rate=rate)

client = web_client()
response = client.get(f"/rates/{requested}")
body = response.json()
assert response.status_code == 200
assert body["date"] == effective
assert body["requested"] == requested
assert body["base"] == "EUR"
assert body["rates"][currency] == rate
=== END AC rates-effective-date ===

=== AC rates-errors ===
Intent: The route returns the declared errors for a missing effective publication and a malformed date.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
assert client.get("/rates/1900-01-01").status_code == 404
assert client.get("/rates/2025-13-01").status_code == 422
=== END AC rates-errors ===

## User Acceptance

- None.

## Guardrails

- Resolve rates using the latest publication date on or before the request.
- Return stored rate text unchanged; do not convert it to floating point.
- Do not hardcode dates, counts, or rates in application code.
