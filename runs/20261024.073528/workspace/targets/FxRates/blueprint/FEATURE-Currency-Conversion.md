# FEATURE: Currency Conversion

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Converts currency amounts using exact decimal arithmetic and half-even rounding. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /convert |
| Consumes    | rates.list |

## Purpose

Convert between EUR and currencies with stored rates using the requested publication date, or the latest publication when no date is supplied. EUR has an implicit rate of one. The returned rate is `rate(to) / rate(from)` and the result is calculated directly from the unrounded stored rates.

## Route

`GET /convert?from=<code>&to=<code>&amount=<amount>[&date=<date>]`

A successful response contains `date`, `from`, `to`, `amount`, `rate`, and `result`. Echo `amount` as the supplied string. Render `rate` as a string with exactly six decimal places, rounded half-even; render `result` as a string with exactly two decimal places, also rounded half-even. Validate `amount` against `[0-9]+(\.[0-9]+)?`. Missing required query parameters, malformed amounts, and malformed or impossible dates return 422. A missing effective publication or unavailable non-EUR currency returns 404.

## Database Interface


- None — persistence is owned by FEATURE-CLI.md, FEATURE-Rate-Loading.md.

## Programmatic Acceptance

=== AC conversion ===
Intent: Conversion echoes the input amount and returns the calculated rate and result for stored rates.

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    date = "2099-01-02"
    from_currency = "QAZ"
    to_currency = "WXY"
    from_rate = "2"
    to_rate = "3"
    amount = "10"
    db.rates.upsert(date=date, currency=from_currency, rate=from_rate)
    db.rates.upsert(date=date, currency=to_currency, rate=to_rate)

client = web_client()
response = client.get(
    "/convert",
    params={"from": from_currency, "to": to_currency, "amount": amount, "date": date},
)
assert response.status_code == 200
body = response.json()
assert body["date"] == date
assert body["from"] == from_currency
assert body["to"] == to_currency
assert body["amount"] == amount
assert body["rate"] == "1.500000"
assert body["result"] == "15.00"
=== END AC conversion ===

=== AC missing-amount ===
Intent: A conversion missing its required amount is rejected with the validation status.

from app_server.testing import web_client

client = web_client()
response = client.get("/convert", params={"from": "EUR", "to": "USD"})
assert response.status_code == 422
=== END AC missing-amount ===

=== AC malformed-amount ===
Intent: A malformed conversion amount is rejected with the validation status.

from app_server.testing import web_client

client = web_client()
response = client.get(
    "/convert",
    params={"from": "EUR", "to": "USD", "amount": "abc"},
)
assert response.status_code == 422
=== END AC malformed-amount ===

=== AC unavailable-currency ===
Intent: A conversion using a currency without an effective rate returns not found.

from app_server.testing import web_client

client = web_client()
response = client.get(
    "/convert",
    params={"from": "EUR", "to": "XXX", "amount": "1"},
)
assert response.status_code == 404
=== END AC unavailable-currency ===

## User Acceptance

- None.

## Guardrails

- Use `decimal.Decimal` for all rate and amount arithmetic; never use binary floating point.
- Compute the result from unrounded source rates, not from the displayed rounded conversion rate.
- Apply half-even rounding at the specified precision.
