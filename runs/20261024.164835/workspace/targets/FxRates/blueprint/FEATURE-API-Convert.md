# FEATURE: API Convert

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Converts amounts between currencies using exact decimal arithmetic. |
| Depends On  | DATABASE.md, FEATURE-API-Foundation.md, FEATURE-ECB-Load.md |
| Provides    | GET /convert |
| Consumes    | rates repository operations |

## Purpose

Convert an amount between two currencies at the effective publication date. EUR has an implicit rate of one unit per euro.

## Database Interface


- None — persistence is owned by FEATURE-API-History.md, FEATURE-API-Rates.md, FEATURE-API-Stats.md, FEATURE-ECB-Load.md.

## Route

### `GET /convert`

Required query parameters are `from`, `to`, and `amount`; `date` is optional. Without a date, use the latest publication. Return 404 when there is no effective publication or a non-EUR currency has no rate on that date. Amounts match `[0-9]+(\.[0-9]+)?` and are echoed as supplied.

Compute the cross-rate as `rate(to) / rate(from)` and the result from the unrounded stored rates. Use exact `Decimal` arithmetic and half-even rounding. Format the rate with six decimal places and the result with two.

## Programmatic Acceptance

=== AC convert-exact-decimal ===
Intent: Conversion returns the effective date and values computed from the supplied rates with the specified decimal rounding.

from decimal import Decimal, ROUND_HALF_EVEN
from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-01-02"
from_code = "ZZZ"
to_code = "YYY"
from_rate = "0.943"
to_rate = "1.25"
amount = "100.25"
with db_session() as db:
    db.rates.replace_rate(date=date, currency=from_code, rate=from_rate)
    db.rates.replace_rate(date=date, currency=to_code, rate=to_rate)

response = web_client().get(
    "/convert",
    params={"from": from_code, "to": to_code, "amount": amount, "date": date},
)
assert response.status_code == 200
body = response.json()
cross_rate = (Decimal(to_rate) / Decimal(from_rate)).quantize(
    Decimal("0.000001"), rounding=ROUND_HALF_EVEN
)
result = (Decimal(amount) * Decimal(to_rate) / Decimal(from_rate)).quantize(
    Decimal("0.01"), rounding=ROUND_HALF_EVEN
)
assert body["date"] == date
assert body["from"] == from_code
assert body["to"] == to_code
assert body["amount"] == amount
assert body["rate"] == format(cross_rate, ".6f")
assert body["result"] == format(result, ".2f")
=== END AC convert-exact-decimal ===

## User Acceptance

- None.

## Guardrails

- Never use floating-point arithmetic for rates or conversions.
- Compute the result from unrounded rates, not the rounded cross-rate.
- Use half-even rounding and the specified fixed decimal places.
- EUR has an implicit rate of one.
