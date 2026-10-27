# FEATURE: Currency Conversion

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Converts an amount between two currencies using exact decimal arithmetic. |
| Depends On  | FEATURE-AppServer.md, DATABASE.md |
| Provides    | GET /convert |
| Consumes    | create_app(), rates repository operations |

## Purpose

Convert an amount from one currency to another using ECB rates, with EUR as the base currency.

## Trigger and workflow

A caller supplies `from`, `to`, and `amount`, with an optional `date`. Missing required parameters, malformed amounts, or malformed dates return `422`. Without a date, use the latest publication. With a date, resolve the latest publication on or before it. Return `404` when no effective publication exists or a requested non-EUR currency lacks a rate on that publication.

EUR has the implicit rate `1`. The conversion rate is `rate(to) / rate(from)`, rounded half-even to six decimal places. The result is calculated directly from the unrounded stored rates and amount, rounded half-even to two decimal places. Both are strings with fixed decimal places; echo the amount text unchanged.

## Database Interface

- `FEATURE-RATE-003` — read: find publications on or before a date - supplies: `requested_date` - returns: `date`, `currency`, `rate`
- `FEATURE-RATE-002` — read: list rates for a publication date - supplies: `date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC convert-decimal-and-rounding ===
Intent: The conversion endpoint echoes its input amount and calculates its rate and result from the fixture rates with the specified rounding.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-08-01"
source_currency = "QAH"
target_currency = "QAI"
amount = "2.00"
source_rate = "2"
target_rate = "5"

with db_session() as db:
    db.rates.upsert(date=date, currency=source_currency, rate=source_rate)
    db.rates.upsert(date=date, currency=target_currency, rate=target_rate)

response = web_client().get(
    "/convert",
    params={"from": source_currency, "to": target_currency, "amount": amount, "date": date},
)
body = response.json()
expected_rate = (Decimal(target_rate) / Decimal(source_rate)).quantize(
    Decimal("0.000001"), rounding=ROUND_HALF_EVEN
)
expected_result = (Decimal(amount) * Decimal(target_rate) / Decimal(source_rate)).quantize(
    Decimal("0.01"), rounding=ROUND_HALF_EVEN
)
assert response.status_code == 200
assert body["date"] == date
assert body["from"] == source_currency
assert body["to"] == target_currency
assert body["amount"] == amount
assert body["rate"] == f"{expected_rate:.6f}"
assert body["result"] == f"{expected_result:.2f}"
=== END AC convert-decimal-and-rounding ===

=== AC convert-validation-and-unknown-currency ===
Intent: The conversion endpoint rejects missing or malformed inputs and returns 404 for a currency without a rate.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
assert client.get("/convert", params={"from": "USD", "to": "EUR"}).status_code == 422
assert client.get(
    "/convert", params={"from": "USD", "to": "EUR", "amount": "abc"}
).status_code == 422
assert client.get(
    "/convert", params={"from": "USD", "to": "EUR", "amount": "1", "date": "2025-13-01"}
).status_code == 422
assert client.get(
    "/convert", params={"from": "USD", "to": "QAJ", "amount": "1", "date": "2099-08-02"}
).status_code == 404
=== END AC convert-validation-and-unknown-currency ===

## User Acceptance

- None.

## Guardrails

- Use `decimal.Decimal` only; never use floating-point arithmetic.
- Compute the result from unrounded source rates, not from the rounded response rate.
- Preserve the caller's amount text in the response.
- Do not embed rates or computed answers in application code.
