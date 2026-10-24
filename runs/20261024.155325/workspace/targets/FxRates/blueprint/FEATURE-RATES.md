# FEATURE: Effective-Date Rates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Returns stored rates for an effective publication date. |
| Depends On  | FEATURE-API-FOUNDATION.md, DATABASE.md |
| Provides    | GET /rates/{date}, GET /rates/latest |
| Consumes    | rates repository operations |

## Purpose

Resolve a requested date to the latest ECB publication on or before that date. Return each stored currency rate as published text. A request before the first publication returns 404. The latest route identifies its request as `latest`.

## Database Interface

- `FEATURE-DATA-003` — read: list rates for a publication - supplies: `date` - returns: `date`, `currency`, `rate`
- `FEATURE-DATA-006` — read: find the effective publication date - supplies: `requested_date` - returns: `date`

## Routes

| Method | Path | Behavior |
|--------|------|----------|
| GET | `/rates/{date}` | Returns rates for the latest publication on or before the valid requested date. |
| GET | `/rates/latest` | Returns the latest publication and marks the request as `latest`. |

## Programmatic Acceptance

Requires: python-package=httpx; scope=test

=== AC rates-effective-date ===
Intent: The date route resolves a weekend-like request to the preceding stored publication and preserves the stored rate text.

from app_server.testing import web_client
from persistence.testing import db_session

publication = "2099-05-01"
requested = "2099-05-02"
currency = "TST"
rate = "1.2300"
with db_session() as db:
    db.rates.upsert(date=publication, currency=currency, rate=rate)
    response = web_client().get(f"/rates/{requested}")
assert response.status_code == 200
body = response.json()
assert body["date"] == publication
assert body["requested"] == requested
assert body["rates"][currency] == rate
=== END AC rates-effective-date ===

=== AC rates-no-publication ===
Intent: A date before every stored publication returns not found.

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    before = db.rates.publication_stats()
    if before:
        earliest = before[0].date
        response = web_client().get(f"/rates/{earliest}/")
    else:
        response = web_client().get("/rates/1900-01-01")
assert response.status_code == 404
=== END AC rates-no-publication ===

=== AC rates-latest ===
Intent: The latest route identifies the latest stored publication as requested.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-05-03"
currency = "TST"
rate = "1.2300"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)
    response = web_client().get("/rates/latest")
assert response.status_code == 200
body = response.json()
assert body["date"] == date
assert body["requested"] == "latest"
=== END AC rates-latest ===

=== AC rates-malformed-date ===
Intent: A malformed calendar date in the path returns unprocessable entity.

from app_server.testing import web_client

response = web_client().get("/rates/2025-13-01")
assert response.status_code == 422
=== END AC rates-malformed-date ===

## User Acceptance

- None.

## Guardrails

- Rates are returned as stored strings; do not convert them to JSON numbers.
- Effective-date resolution is inclusive of the requested date.
