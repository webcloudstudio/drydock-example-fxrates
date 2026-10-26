# FEATURE: Currency Conversion

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Converts amounts between currencies using effective ECB rates. |
| Depends On  | ARCHITECTURE.md, DATABASE.md, FEATURE-HistoryLoading.md |
| Provides    | GET /convert |
| Consumes    | rates.effective_rates, rates.by_date |

## Purpose

Convert an amount from one currency to another. EUR is the base currency with implicit rate one.

## Behavior

- Require `from`, `to`, and `amount`; optional `date` defaults to the latest publication date.
- Accept amount strings matching `[0-9]+(\.[0-9]+)?`; malformed or missing inputs return 422.
- Apply the effective publication date rule. Return 404 if no publication exists or a non-EUR currency has no rate for that date.
- Compute the conversion rate exactly as target rate divided by source rate. Round half to even to six decimal places and return exactly six decimals.
- Compute the result from the exact stored rates, not the rounded display rate. Round half to even to two decimal places and return exactly two decimals.
- Echo the amount as supplied. Return JSON fields `date`, `from`, `to`, `amount`, `rate`, and `result`.
- A missing currency rate is not inferred from another date.

## Database Interface

- `FEATURE-RATE-002` — read: find rates on or before a date - supplies: `as_of` - returns: `date`, `currency`, `rate`
- `FEATURE-RATE-003` — read: list rates for one date - supplies: `date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC conversion-route ===
Intent: The conversion route returns a successful response and echoes the supplied amount and currency codes.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-03-01"
amount = "2.00"
source_rate = "2"
target_rate = "5"

with db_session() as db:
    db.rates.upsert(date=date, currency="AAA", rate=source_rate)
    db.rates.upsert(date=date, currency="ZZZ", rate=target_rate)

response = web_client().get(
    "/convert",
    params={"from": "AAA", "to": "ZZZ", "amount": amount, "date": date},
)
assert response.status_code == 200
body = response.json()
assert body["amount"] == amount
assert body["from"] == "AAA"
assert body["to"] == "ZZZ"
assert body["date"] == date
=== END AC conversion-route ===

=== AC conversion-rounding ===
Intent: The conversion rate and result use exact source rates and half-even rounding at their specified precisions.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-03-02"
amount = "2.00"
source_rate = "2"
target_rate = "5"
expected_rate = (Decimal(target_rate) / Decimal(source_rate)).quantize(
    Decimal("0.000001"), rounding=ROUND_HALF_EVEN
)
expected_result = (Decimal(amount) * Decimal(target_rate) / Decimal(source_rate)).quantize(
    Decimal("0.01"), rounding=ROUND_HALF_EVEN
)

with db_session() as db:
    db.rates.upsert(date=date, currency="AAA", rate=source_rate)
    db.rates.upsert(date=date, currency="ZZZ", rate=target_rate)

response = web_client().get(
    "/convert",
    params={"from": "AAA", "to": "ZZZ", "amount": amount, "date": date},
)
assert response.status_code == 200
body = response.json()
assert body["rate"] == f"{expected_rate:.6f}"
assert body["result"] == f"{expected_result:.2f}"
=== END AC conversion-rounding ===

=== AC conversion-errors ===
Intent: The conversion route rejects a missing or malformed amount and returns not found for an unavailable currency.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    db.rates.upsert(date="2099-03-03", currency="AAA", rate="2")

client = web_client()
assert client.get("/convert", params={"from": "AAA", "to": "ZZZ"}).status_code == 422
assert client.get(
    "/convert",
    params={"from": "AAA", "to": "ZZZ", "amount": "abc"},
).status_code == 422
assert client.get(
    "/convert",
    params={"from": "AAA", "to": "ZZZ", "amount": "1"},
).status_code == 404
=== END AC conversion-errors ===

## User Acceptance

- None.

## Guardrails

- Use decimal arithmetic only; never use floating point.
- Compute the result from exact stored rates before rounding.
