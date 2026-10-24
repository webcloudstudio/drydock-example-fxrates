# FEATURE: Effective Date Rates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Retrieves stored exchange rates for a requested or latest effective publication date. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /rates/{date}, GET /rates/latest |
| Consumes    | rates.list |

## Purpose

Return all rates stored for the latest publication on or before the requested date. EUR is the base and has an implicit rate of 1; only currencies with stored rates appear in the response.

## Workflow

- `GET /rates/{date}` accepts a real calendar date in `YYYY-MM-DD` form. It returns the effective publication date, the original requested date, base `EUR`, and the rates for that publication.
- `GET /rates/latest` returns the latest publication and uses `"latest"` as the requested value.
- Return 404 when no publication exists on or before the requested date. Return 422 for a malformed date.

## Database Interface

- `FEATURE-RATE-002` — read: list rates for a publication date - supplies: `date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC rates-effective-date ===
Intent: The date endpoint resolves a seeded date to the latest available publication and returns its stored rate text.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2001-01-02"
requested = "2001-01-03"
currency = "USD"
rate = "1.2345"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get(f"/rates/{requested}")
body = response.json()
assert response.status_code == 200
assert body["date"] == date
assert body["requested"] == requested
assert body["base"] == "EUR"
assert body["rates"][currency] == rate
=== END AC rates-effective-date ===

=== AC rates-latest ===
Intent: The latest endpoint returns the newest publication and its stored rates.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2001-01-04"
currency = "JPY"
rate = "120.5"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get("/rates/latest")
body = response.json()
assert response.status_code == 200
assert body["date"] == date
assert body["requested"] == "latest"
assert body["rates"][currency] == rate
=== END AC rates-latest ===

=== AC rates-no-publication ===
Intent: A date before every stored publication returns 404.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2001-01-06"
currency = "CAD"
rate = "1.4"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get("/rates/2000-12-31")
assert response.status_code == 404
=== END AC rates-no-publication ===

=== AC rates-malformed-date ===
Intent: A malformed date returns 422.

from app_server.testing import web_client

response = web_client().get("/rates/2025-13-01")
assert response.status_code == 422
=== END AC rates-malformed-date ===

## User Acceptance

- None.

## Guardrails

- Preserve stored rate text in JSON strings.
- Resolve dates using the latest publication on or before the requested date.
- Do not include currencies without a stored rate for the effective publication.
- Reach persistence only through the declared persistence library.
