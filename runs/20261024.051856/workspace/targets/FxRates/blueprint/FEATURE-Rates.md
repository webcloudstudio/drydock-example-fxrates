# FEATURE: Effective-Date Rates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Resolves requested and latest publication dates to their stored ECB rates. |
| Depends On  | FEATURE-API-Foundation.md, DATABASE.md |
| Provides    | GET /rates/{date}, GET /rates/latest |
| Consumes    | rates repository operations |

## Purpose

Expose the ECB rates for a requested date using the latest publication on or before that date. Also expose the latest publication directly.

## Routes

| Method | Path | Behavior |
|--------|------|----------|
| GET | `/rates/{date}` | Resolve the effective publication date and return its rates. |
| GET | `/rates/latest` | Return rates from the latest publication, with `requested` set to `latest`. |

The response includes the effective `date`, the original `requested` value, `base` set to `EUR`, and a `rates` object containing every currency stored for the effective date. Rate values remain strings exactly as stored.

If no publication exists on or before the requested date, return 404.

## Programmatic Acceptance

=== AC date-resolves-to-effective-publication ===
Intent: The requested-date route returns the effective stored publication and preserves the requested date.

from persistence.testing import db_session
from app_server.testing import web_client

date = "2098-01-02"
requested = "2098-01-03"
currency = "ZZZ"
rate = "7.654321"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

client = web_client()
response = client.get(f"/rates/{requested}")
assert response.status_code == 200
body = response.json()
assert body["date"] == date
assert body["requested"] == requested
assert body["base"] == "EUR"
assert body["rates"][currency] == rate
=== END AC date-resolves-to-effective-publication ===

=== AC latest-rates-route-works ===
Intent: The latest route returns a successful response and the latest stored publication.

from persistence.testing import db_session
from app_server.testing import web_client

date = "2098-02-04"
currency = "ZZY"
rate = "8.765432"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

client = web_client()
response = client.get("/rates/latest")
assert response.status_code == 200
body = response.json()
assert body["date"] == date
assert body["requested"] == "latest"
assert body["base"] == "EUR"
assert body["rates"][currency] == rate
=== END AC latest-rates-route-works ===

=== AC no-publication-before-date-is-not-found ===
Intent: A date with no earlier stored publication returns 404.

from app_server.testing import web_client

response = web_client().get("/rates/1900-01-01")
assert response.status_code == 404
=== END AC no-publication-before-date-is-not-found ===

## User Acceptance

- None.

## Guardrails

- Effective-date lookup uses stored publication dates and never a hardcoded rate, date, or computed answer.
- EUR is the implicit base; only stored currencies with rates for the effective publication are returned.
