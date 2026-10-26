# FEATURE: Currency Conversion

| Field | Value |
|-------|-------|
| Version | 20261025 V1 |
| Description | Convert amounts between currencies using effective ECB rates. |
| Depends On | FEATURE-ApiFoundation.md, DATABASE.md |
| Provides | GET /convert |
| Consumes | rates repository operations |

## Purpose

`GET /convert` accepts required `from`, `to`, and `amount` parameters and an optional date. Without a date it uses the latest publication. EUR has the implicit rate one. Return the effective date, input currencies, amount text, conversion rate, and result.

Compute with `decimal.Decimal`. The conversion rate is `rate(to) / rate(from)`, rounded half to even to six decimal places and formatted with six decimals. The result is computed from the unrounded rates and amount, rounded half to even to two decimal places and formatted with two decimals.

## Database Interface


- None — persistence is owned by FEATURE-InitializeRates.md, FEATURE-LoadHistory.md.

## Programmatic Acceptance

=== AC conversion_route ===
Intent: Conversion returns the supplied amount and currencies and a result derived from the stored rates.
Requires: python-package=httpx; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from persistence.testing import db_session
from app_server.testing import web_client

date = "2099-01-02"
source = "ZZZ"
target = "YYY"
source_rate = "2.00"
target_rate = "5.00"
amount = "2.00"
with db_session() as db:
    db.rates.upsert(date=date, currency=source, rate=source_rate)
    db.rates.upsert(date=date, currency=target, rate=target_rate)

response = web_client().get(
    "/convert",
    params={"from": source, "to": target, "amount": amount, "date": date},
)
assert response.status_code == 200
body = response.json()
expected_rate = (Decimal(target_rate) / Decimal(source_rate)).quantize(
    Decimal("0.000001"), rounding=ROUND_HALF_EVEN
)
expected_result = (Decimal(amount) * Decimal(target_rate) / Decimal(source_rate)).quantize(
    Decimal("0.01"), rounding=ROUND_HALF_EVEN
)
assert body["date"] == date
assert body["from"] == source
assert body["to"] == target
assert body["amount"] == amount
assert body["rate"] == f"{expected_rate:.6f}"
assert body["result"] == f"{expected_result:.2f}"
=== END AC conversion_route ===

=== AC conversion_requires_parameters ===
Intent: A conversion missing its required amount returns 422.
Requires: python-package=httpx; scope=test

from app_server.testing import web_client

response = web_client().get("/convert", params={"from": "EUR", "to": "EUR"})
assert response.status_code == 422
=== END AC conversion_requires_parameters ===

## User Acceptance

- None.

## Guardrails

- Validate amount syntax as `[0-9]+(\\.[0-9]+)?`.
- Never use floating-point arithmetic.
- Unknown currencies or unavailable rates return 404; malformed amount or missing parameters return 422.
- Do not compute the result from the rounded conversion rate.
