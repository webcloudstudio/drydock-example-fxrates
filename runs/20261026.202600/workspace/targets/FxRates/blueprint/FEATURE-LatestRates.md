# FEATURE: Latest Publication Rates

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Retrieves rates from the latest stored publication. |
| Depends On  | FEATURE-AppServer.md, DATABASE.md |
| Provides    | GET /rates/latest |
| Consumes    | create_app(), rates repository operations |

## Purpose

Return all stored rates for the latest publication date, identifying the request as `latest`.

## Trigger and workflow

A caller requests `GET /rates/latest`. Find the most recent publication date and retrieve its rates. Return `404` if no publication exists.

## Database Interface

- `FEATURE-RATE-003` — read: find publications on or before a date - supplies: `requested_date` - returns: `date`, `currency`, `rate`
- `FEATURE-RATE-002` — read: list rates for a publication date - supplies: `date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC latest-rates-response ===
Intent: The latest-rates route returns the stored rates for the latest publication.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-07-02"
currency = "QAG"
rate = "7.25"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get("/rates/latest")
body = response.json()
assert response.status_code == 200
assert body["date"] == date
assert body["requested"] == "latest"
assert body["base"] == "EUR"
assert body["rates"][currency] == rate
=== END AC latest-rates-response ===

=== AC latest-rates-empty ===
Intent: The latest-rates route returns 404 when there is no publication.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

assert web_client().get("/rates/latest").status_code == 404
=== END AC latest-rates-empty ===

## User Acceptance

- None.

## Guardrails

- Derive the latest date and rates from repository queries.
- Preserve stored rate text exactly.
