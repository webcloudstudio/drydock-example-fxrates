# FEATURE: Effective-Date Rates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Resolves rate requests to the latest available ECB publication date. |
| Depends On  | DATABASE.md |
| Provides    | GET /rates/{date}, GET /rates/latest |
| Consumes    | rates repository operations |

## Purpose

Return all rates stored for the latest publication on or before a requested date. The latest route uses the most recent publication and reports `"latest"` as the requested value. EUR is the base; published rates are returned as stored text. Return 404 if no publication exists on or before the requested date.

## Database Interface

- `FEATURE-RATE-002` — read: list rates with optional date and currency filters - supplies: `date`, `currency` - returns: `id`, `date`, `currency`, `rate`

## Programmatic Acceptance

Requires: python-package=httpx; scope=test

=== AC rates-effective-date ===
Intent: A date request returns the rates for the most recent publication on or before the requested date.

from persistence.testing import db_session
from app_server.testing import web_client

publication = "2099-01-02"
requested = "2099-01-03"
currency = "ZZZ"
rate = "1.2300"
with db_session() as db:
    db.rates.upsert(date=publication, currency=currency, rate=rate)

response = web_client().get(f"/rates/{requested}")
body = response.json()
assert response.status_code == 200
assert body["date"] == publication
assert body["requested"] == requested
assert body["rates"][currency] == rate
=== END AC rates-effective-date ===

=== AC rates-no-prior-publication ===
Intent: A date before every stored publication returns not found.

from persistence.testing import db_session
from app_server.testing import web_client

publication = "2099-01-02"
currency = "ZZZ"
with db_session() as db:
    db.rates.upsert(date=publication, currency=currency, rate="1.23")

response = web_client().get("/rates/1999-01-01")
assert response.status_code == 404
=== END AC rates-no-prior-publication ===

=== AC rates-latest ===
Intent: The latest route reports the latest stored publication and its rates.

from persistence.testing import db_session
from app_server.testing import web_client

publication = "2099-01-02"
currency = "ZZZ"
rate = "1.2300"
with db_session() as db:
    db.rates.upsert(date=publication, currency=currency, rate=rate)

response = web_client().get("/rates/latest")
body = response.json()
assert response.status_code == 200
assert body["date"] == publication
assert body["requested"] == "latest"
assert body["rates"][currency] == rate
=== END AC rates-latest ===

## User Acceptance

- None.

## Guardrails

- Rate values remain the ECB-published text.
- Resolve effective dates from stored publications; do not hardcode rates or dates.
