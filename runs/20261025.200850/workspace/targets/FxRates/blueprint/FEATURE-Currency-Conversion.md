# FEATURE: Currency Conversion

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Converts an amount between currencies using effective ECB rates and exact decimal arithmetic. |
| Depends On  | FEATURE-API-Foundation.md, DATABASE.md |
| Provides    | GET /convert |
| Consumes    | rates repository operations |

## Purpose

Convert an amount from one currency to another using EUR as the base. If `date` is omitted, use the latest publication.

## Request and Response

`GET /convert` requires `from`, `to`, and `amount`, with optional `date`. Amounts must match `[0-9]+(\.[0-9]+)?` and are echoed as supplied. The response includes effective date, source and target currencies, amount, conversion rate, and result as strings.

Compute the conversion rate as `rate(to) / rate(from)` using exact decimal arithmetic, rounded half to even to six decimal places. Compute the result from the unrounded rates, rounded half to even to two decimal places. Return 404 when no effective publication exists or a non-EUR currency has no rate on that date. Malformed dates, amounts, or missing required parameters return 422.

## Database Interface

- `FEATURE-RATE-003` — read: list stored rates - supplies: `currency`, `start_date`, `end_date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC conversion-route ===
Intent: Conversion returns a reachable response with the supplied amount and currencies using the effective stored rates.

from app_server.testing import web_client
from persistence.testing import db_session

day = "2099-01-02"
source = "XTS"
target = "XTU"
amount = "2.00"
source_rate = "2"
target_rate = "5"
with db_session() as db:
    db.rates.upsert(date=day, currency=source, rate=source_rate)
    db.rates.upsert(date=day, currency=target, rate=target_rate)

response = web_client().get(
    "/convert",
    params={"from": source, "to": target, "amount": amount, "date": day},
)
assert response.status_code == 200
body = response.json()
assert body["date"] == day
assert body["from"] == source
assert body["to"] == target
assert body["amount"] == amount
assert body["rate"] == "2.500000"
assert body["result"] == "10.00"
=== END AC conversion-route ===

=== AC conversion-validation-errors ===
Intent: Missing or malformed inputs return 422, while an unknown currency returns 404.

from app_server.testing import web_client
from persistence.testing import db_session

day = "2099-01-02"
with db_session() as db:
    db.rates.upsert(date=day, currency="XTS", rate="1.2")

client = web_client()
assert client.get("/convert").status_code == 422
assert client.get("/convert", params={"from": "XTS", "to": "XXX", "amount": "1"}).status_code == 404
assert client.get("/convert", params={"from": "XTS", "to": "XTS", "amount": "abc"}).status_code == 422
assert client.get(
    "/convert",
    params={"from": "XTS", "to": "XTS", "amount": "1", "date": "2099-13-01"},
).status_code == 422
=== END AC conversion-validation-errors ===

## User Acceptance

- None.

## Guardrails

- Use `decimal`; never use floating-point arithmetic.
- Compute the result from unrounded stored rates, not the displayed rounded conversion rate.
- Apply half-even rounding and the specified fixed decimal-place formatting.
