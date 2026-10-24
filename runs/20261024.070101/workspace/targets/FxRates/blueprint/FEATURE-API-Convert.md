# FEATURE: Currency Conversion

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Converts an amount between currencies using exact decimal arithmetic. |
| Depends On  | DATABASE.md |
| Provides    | GET /convert |
| Consumes    | rates repository operations |

## Purpose

Convert using rates for the latest publication on or before the supplied date, or the latest publication when no date is supplied. EUR has implicit rate `1`. Require `from`, `to`, and `amount`. Amounts must match `[0-9]+(\.[0-9]+)?`. Return the rate rounded half-even to six decimal places and the result rounded half-even to two places; compute the result from unrounded stored rates.

## Database Interface

- `FEATURE-RATE-002` — read: list rates with optional date and currency filters - supplies: `date`, `currency` - returns: `id`, `date`, `currency`, `rate`

## Programmatic Acceptance

Requires: python-package=httpx; scope=test

=== AC convert-exact-decimal ===
Intent: Conversion uses exact rate values and echoes the supplied amount and currencies.

from persistence.testing import db_session
from app_server.testing import web_client

publication = "2099-01-02"
source = "AAA"
target = "BBB"
source_rate = "3"
target_rate = "2"
amount = "10.00"
with db_session() as db:
    db.rates.upsert(date=publication, currency=source, rate=source_rate)
    db.rates.upsert(date=publication, currency=target, rate=target_rate)

response = web_client().get(
    "/convert",
    params={"from": source, "to": target, "amount": amount, "date": publication},
)
body = response.json()
assert response.status_code == 200
assert body["date"] == publication
assert body["from"] == source
assert body["to"] == target
assert body["amount"] == amount
assert body["rate"] == "0.666667"
assert body["result"] == "6.67"
=== END AC convert-exact-decimal ===

=== AC convert-invalid-amount ===
Intent: A malformed amount is rejected with the request-validation status.

from app_server.testing import web_client

response = web_client().get(
    "/convert", params={"from": "EUR", "to": "EUR", "amount": "bad"}
)
assert response.status_code == 422
=== END AC convert-invalid-amount ===

=== AC convert-missing-amount ===
Intent: A missing required amount is rejected with the request-validation status.

from app_server.testing import web_client

response = web_client().get("/convert", params={"from": "EUR", "to": "EUR"})
assert response.status_code == 422
=== END AC convert-missing-amount ===

=== AC convert-unknown-currency ===
Intent: A currency without a rate on the effective date returns not found.

from persistence.testing import db_session
from app_server.testing import web_client

publication = "2099-01-02"
currency = "AAA"
with db_session() as db:
    db.rates.upsert(date=publication, currency=currency, rate="1.23")

response = web_client().get(
    "/convert",
    params={"from": currency, "to": "ZZZ", "amount": "1", "date": publication},
)
assert response.status_code == 404
=== END AC convert-unknown-currency ===

## User Acceptance

- None.

## Guardrails

- Use `decimal.Decimal`; never use floating-point arithmetic for rates or results.
- The result is calculated from unrounded rates, not the displayed rounded conversion rate.
