# FEATURE: Currency Conversion

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Converts amounts between currencies using exact decimal arithmetic. |
| Depends On  | FEATURE-API-FOUNDATION.md, DATABASE.md |
| Provides    | GET /convert |
| Consumes    | rates repository operations |

## Purpose

Convert an amount from one currency to another using the latest publication when no date is supplied, or the latest publication on or before the supplied date. EUR has implicit rate one. Use exact Decimal arithmetic. The response rate is rounded half to even to six decimal places; the result is calculated from the unrounded rates and rounded half to even to two decimal places.

## Database Interface


- `FEATURE-DATA-002` — read: rates.get - supplies: `date`, `currency` - returns: `date`, `currency`, `rate`

## Route

| Method | Path | Behavior |
|--------|------|----------|
| GET | `/convert` | Converts a valid amount between currencies, optionally at an effective date; omitted date uses the latest publication. |

## Values

- Amount must match `[0-9]+(\.[0-9]+)?` and is echoed as supplied as a JSON string.
- The response rate is `rate(to) / rate(from)`, rendered with exactly six decimal places.
- The result is `amount × rate(to) / rate(from)`, rendered with exactly two decimal places.
- Both values use half-even rounding.
- A non-EUR currency without a rate on the effective date returns 404. Unknown currencies return 404.
- Malformed dates, malformed amounts, and missing required parameters return 422.

## Programmatic Acceptance

Requires: python-package=httpx; scope=test

=== AC convert-route ===
Intent: The conversion route accepts the required query values and echoes the supplied amount and currencies.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-06-01"
currency = "TST"
rate = "1.2500"
amount = "2.00"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)
    response = web_client().get(
        "/convert",
        params={"from": currency, "to": currency, "amount": amount},
    )
assert response.status_code == 200
body = response.json()
assert body["date"] == date
assert body["from"] == currency
assert body["to"] == currency
assert body["amount"] == amount
=== END AC convert-route ===

=== AC convert-rounding-shape ===
Intent: Conversion outputs are strings with the declared fixed decimal places.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-06-02"
amount = "2"
with db_session() as db:
    db.rates.upsert(date=date, currency="TST", rate="1.25")
    db.rates.upsert(date=date, currency="OTH", rate="2.5")
    response = web_client().get(
        "/convert",
        params={"from": "TST", "to": "OTH", "amount": amount},
    )
assert response.status_code == 200
body = response.json()
assert isinstance(body["rate"], str)
assert len(body["rate"].partition(".")[2]) == 6
assert isinstance(body["result"], str)
assert len(body["result"].partition(".")[2]) == 2
=== END AC convert-rounding-shape ===

=== AC convert-missing-rate ===
Intent: A conversion for a currency without a rate on the effective date returns not found.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-06-03"
amount = "1"
with db_session() as db:
    db.rates.upsert(date=date, currency="TST", rate="1")
    response = web_client().get(
        "/convert",
        params={"from": "TST", "to": "ABS", "amount": amount},
    )
assert response.status_code == 404
=== END AC convert-missing-rate ===

=== AC convert-invalid-amount ===
Intent: A malformed amount returns unprocessable entity.

from app_server.testing import web_client

response = web_client().get(
    "/convert",
    params={"from": "EUR", "to": "EUR", "amount": "abc"},
)
assert response.status_code == 422
=== END AC convert-invalid-amount ===

=== AC convert-missing-parameter ===
Intent: A missing required amount returns unprocessable entity.

from app_server.testing import web_client

response = web_client().get("/convert", params={"from": "EUR", "to": "EUR"})
assert response.status_code == 422
=== END AC convert-missing-parameter ===

## User Acceptance

- None.

## Guardrails

- Never use floating-point arithmetic for rates or conversion values.
- Compute the result from unrounded stored rates, not from the rounded response rate.
