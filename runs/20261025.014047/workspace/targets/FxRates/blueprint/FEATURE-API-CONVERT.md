# FEATURE: API Currency Conversion

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Converts amounts between currencies using effective ECB rates and exact decimal arithmetic. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /convert |
| Consumes    | rates.get, rates.list |

## Purpose

Allow callers to convert an amount from one currency to another, using the latest publication date on or before the requested date. If no date is supplied, use the latest publication date.

## Trigger and workflow

`GET /convert` requires `from`, `to`, and `amount` query parameters; `date` is optional. EUR has an implicit rate of one. For other currencies, resolve rates from the selected publication date. Return 404 if either requested non-EUR currency has no rate on that date.

Validate dates and amounts according to the API contract. Amounts must match `[0-9]+(\.[0-9]+)?`. Calculate with `decimal.Decimal`, using half-even rounding: return the conversion rate with six decimal places and the result with two decimal places. Calculate the result from the unrounded rate.

The JSON response contains `date`, `from`, `to`, `amount`, `rate`, and `result`. Echo the amount as supplied.

## Programmatic Acceptance

=== AC convert-request-contract ===
Intent: The conversion endpoint accepts a valid request and echoes its supplied date, currencies, and amount.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-12-30"
source_currency = "ZZZ"
target_currency = "YYY"
source_rate = "2"
target_rate = "5"
amount = "12.50"

with db_session() as db:
    db.rates.upsert(date=date, currency=source_currency, rate=source_rate)
    db.rates.upsert(date=date, currency=target_currency, rate=target_rate)

client = web_client()
response = client.get(
    "/convert",
    params={
        "from": source_currency,
        "to": target_currency,
        "amount": amount,
        "date": date,
    },
)
assert response.status_code == 200
body = response.json()
assert body["date"] == date
assert body["from"] == source_currency
assert body["to"] == target_currency
assert body["amount"] == amount
assert isinstance(body["rate"], str)
assert isinstance(body["result"], str)
=== END AC convert-request-contract ===

=== AC convert-rejects-invalid-requests ===
Intent: The conversion endpoint rejects missing or malformed required inputs and unknown currencies with the specified statuses.

from app_server.testing import web_client

client = web_client()
assert client.get("/convert", params={"from": "EUR", "to": "EUR"}).status_code == 422
assert client.get(
    "/convert",
    params={"from": "EUR", "to": "EUR", "amount": "bad"},
).status_code == 422
assert client.get(
    "/convert",
    params={"from": "EUR", "to": "ZZZ", "amount": "1"},
).status_code == 404
=== END AC convert-rejects-invalid-requests ===

## User Acceptance

- None.

## Guardrails

- Use `Decimal` for all rate and amount arithmetic; never use floating point.
- Round half to even, formatting the rate to six decimal places and the result to two.
- Compute the result from the exact rates, not from the rounded response rate.
- Return 422 for malformed dates or amounts and missing required parameters; return 404 for unavailable currencies or dates.
