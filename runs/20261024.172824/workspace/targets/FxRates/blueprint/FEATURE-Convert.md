# FEATURE: Currency Conversion

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Converts an amount between currencies using rates from an effective publication date. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /convert |
| Consumes    | rates.list |

## Purpose

Convert between any two currencies using EUR as the base. If no date is supplied, use the latest publication. If a date is supplied, resolve it to the latest publication on or before that date.

## Workflow

Require `from`, `to`, and `amount`. Amount must match `[0-9]+(\.[0-9]+)?` and is echoed as supplied. EUR has an implicit rate of 1. Compute `rate(to) / rate(from)` exactly and round half to even to six decimal places. Compute `amount × rate(to) / rate(from)` from the unrounded rates and round half to even to two decimal places. Return both as strings with exactly six and two decimal places respectively.

Return 404 if there is no effective publication or a non-EUR currency has no rate for it. Return 422 for a malformed amount or date, or a missing required parameter.

## Database Interface

- `FEATURE-RATE-002` — read: list rates for a publication date - supplies: `date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC convert-exact-values ===
Intent: Conversion returns the supplied amount and the exact same-currency ratio with contract precision.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2001-01-07"
currency = "USD"
rate = "1.25"
amount = "2.50"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get(
    "/convert",
    params={"from": currency, "to": currency, "amount": amount, "date": date},
)
body = response.json()
assert response.status_code == 200
assert body["date"] == date
assert body["from"] == currency
assert body["to"] == currency
assert body["amount"] == amount
assert body["rate"] == "1.000000"
assert body["result"] == "2.50"
=== END AC convert-exact-values ===

=== AC convert-eur-base ===
Intent: EUR conversions use the implicit base rate and return the supplied amount rounded to the result precision.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2001-01-08"
currency = "GBP"
rate = "0.80"
amount = "10"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get(
    "/convert",
    params={"from": "EUR", "to": currency, "amount": amount, "date": date},
)
body = response.json()
assert response.status_code == 200
assert body["date"] == date
assert body["rate"] == "0.800000"
assert body["result"] == "8.00"
=== END AC convert-eur-base ===

=== AC convert-invalid-amount ===
Intent: A malformed amount is rejected with 422.

from app_server.testing import web_client

response = web_client().get(
    "/convert",
    params={"from": "EUR", "to": "USD", "amount": "abc"},
)
assert response.status_code == 422
=== END AC convert-invalid-amount ===

=== AC convert-missing-parameter ===
Intent: A missing required conversion parameter is rejected with 422.

from app_server.testing import web_client

response = web_client().get("/convert", params={"from": "EUR", "to": "USD"})
assert response.status_code == 422
=== END AC convert-missing-parameter ===

=== AC convert-unknown-currency ===
Intent: An unavailable currency is rejected with 404.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2001-01-09"
currency = "USD"
rate = "1.2"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get(
    "/convert",
    params={"from": currency, "to": "XXX", "amount": "1", "date": date},
)
assert response.status_code == 404
=== END AC convert-unknown-currency ===

## User Acceptance

- None.

## Guardrails

- Use exact decimal arithmetic; never use floating point.
- Calculate the result from unrounded rates, not from the rounded response rate.
- Round using half to even and preserve the specified decimal places in response strings.
- Reach persistence only through the declared persistence library.
