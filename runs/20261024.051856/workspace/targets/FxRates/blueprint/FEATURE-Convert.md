# FEATURE: Currency Conversion

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Converts an amount between currencies using exact decimal arithmetic. |
| Depends On  | FEATURE-API-Foundation.md, DATABASE.md |
| Provides    | GET /convert |
| Consumes    | rates repository operations |

## Purpose

Convert an amount from one currency to another at the latest effective publication date, or at the latest publication on or before an optional requested date.

## Route

`GET /convert?from=<code>&to=<code>&amount=<amount>[&date=<date>]`

The response contains the effective date, the supplied `from`, `to`, and `amount`, plus `rate` and `result`. `amount` is echoed as a string. The rate is `rate(to) / rate(from)`, rounded to six decimal places using half-even rounding. The result is calculated directly from the stored rates and amount, not from the rounded rate, then rounded to two decimal places using half-even rounding. Both computed values are strings with fixed decimal places.

EUR has an implicit rate of one. A non-EUR currency without a rate on the effective date returns 404. Malformed amounts, malformed dates, or missing required query parameters return 422.

## Programmatic Acceptance

=== AC convert-route-returns-computed-values ===
Intent: The conversion route returns the echoed inputs and values derived from the supplied rates.

from decimal import Decimal, ROUND_HALF_EVEN
from persistence.testing import db_session
from app_server.testing import web_client

date = "2098-03-04"
source_currency = "ZZX"
target_currency = "ZZW"
source_rate_text = "3.125"
target_rate_text = "6.75"
amount_text = "10.10"
with db_session() as db:
    db.rates.upsert(date=date, currency=source_currency, rate=source_rate_text)
    db.rates.upsert(date=date, currency=target_currency, rate=target_rate_text)

client = web_client()
response = client.get(
    "/convert",
    params={"from": source_currency, "to": target_currency, "amount": amount_text, "date": date},
)
assert response.status_code == 200
body = response.json()
expected_rate = (Decimal(target_rate_text) / Decimal(source_rate_text)).quantize(
    Decimal("0.000001"), rounding=ROUND_HALF_EVEN
)
expected_result = (Decimal(amount_text) * Decimal(target_rate_text) / Decimal(source_rate_text)).quantize(
    Decimal("0.01"), rounding=ROUND_HALF_EVEN
)
assert body["date"] == date
assert body["from"] == source_currency
assert body["to"] == target_currency
assert body["amount"] == amount_text
assert body["rate"] == f"{expected_rate:.6f}"
assert body["result"] == f"{expected_result:.2f}"
=== END AC convert-route-returns-computed-values ===

=== AC euro-conversion-uses-implicit-unit-rate ===
Intent: EUR conversions use the implicit unit rate without requiring an EUR row.

from persistence.testing import db_session
from app_server.testing import web_client

date = "2098-03-05"
currency = "ZZV"
rate = "2.5"
amount = "4"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get(
    "/convert", params={"from": "EUR", "to": currency, "amount": amount, "date": date}
)
assert response.status_code == 200
body = response.json()
assert body["amount"] == amount
assert body["rate"] == rate + "0" * (6 - len(rate.rsplit(".", 1)[1])) + ("0.000000" if "." not in rate else "")
=== END AC euro-conversion-uses-implicit-unit-rate ===

## User Acceptance

- None.

## Guardrails

- Use `decimal.Decimal` for rate and amount arithmetic, never binary floating point.
- Compute the result from unrounded source and target rates, independently of the rounded response rate.
