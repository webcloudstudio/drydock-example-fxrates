# FEATURE: Currency Conversion

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Converts amounts between currencies using exact decimal arithmetic. |
| Depends On  | DATABASE.md, ARCHITECTURE.md |
| Provides    | GET /convert |
| Consumes    | `FEATURE-RATE-001` rates.upsert, `FEATURE-RATE-002` rates.list_date, `FEATURE-RATE-005` rates.list_all |

## Purpose

Convert an amount from one currency to another using rates for the effective publication date. EUR has the implicit rate `1`.

## Workflow

`GET /convert` requires `from`, `to`, and `amount`; `date` is optional and defaults to the latest publication. Amounts must match `[0-9]+(\.[0-9]+)?` and are echoed as supplied. Malformed or missing values return 422. A missing effective publication or unavailable non-EUR currency returns 404.

The response includes effective date, source and destination currencies, amount, rate, and result. Compute `rate = rate(to) / rate(from)` exactly from stored text and round half-even to six decimal places. Compute the result from the unrounded ratio and input amount, rounding half-even to two decimal places. Both results are fixed-width decimal strings.

## Database Interface

- `FEATURE-RATE-002` — read: list rates for a publication date - supplies: `date` - returns: `date`, `currency`, `rate`
- `FEATURE-RATE-005` — read: list all rates - supplies: — - returns: `date`, `currency`, `rate`

## Guardrails

- Use `decimal.Decimal` throughout; never use binary floating point.
- Compute the result from the unrounded conversion ratio.
- Keep request amount text unchanged in the response.

## Programmatic Acceptance

=== AC convert-route ===
Intent: The conversion route is reachable and returns the supplied amount with currency values from stored rate text.

from persistence.testing import db_session
from app_server.testing import web_client

date = "2098-04-02"
from_code = "AAA"
to_code = "BBB"
amount = "10.25"
from_rate = "2"
to_rate = "3"
with db_session() as db:
    db.rates.upsert(date=date, currency=from_code, rate=from_rate)
    db.rates.upsert(date=date, currency=to_code, rate=to_rate)
    response = web_client().get(
        "/convert",
        params={"from": from_code, "to": to_code, "amount": amount, "date": date},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["date"] == date
    assert body["from"] == from_code
    assert body["to"] == to_code
    assert body["amount"] == amount
    assert body["rate"] == "1.500000"
    assert body["result"] == "15.38"
=== END AC convert-route ===

=== AC convert-eur ===
Intent: EUR is accepted as the implicit base currency when converting to a stored currency.

from persistence.testing import db_session
from app_server.testing import web_client

date = "2098-04-03"
currency = "ZZZ"
amount = "2"
rate = "1.25"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)
    response = web_client().get(
        "/convert",
        params={"from": "EUR", "to": currency, "amount": amount, "date": date},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["from"] == "EUR"
    assert body["to"] == currency
=== END AC convert-eur ===

=== AC convert-errors ===
Intent: The conversion route returns the declared statuses for unavailable currencies, missing inputs, and malformed amounts or dates.

from app_server.testing import web_client

client = web_client()
assert client.get("/convert", params={"from": "USD", "to": "XXX", "amount": "1"}).status_code == 404
assert client.get("/convert", params={"from": "USD", "to": "GBP"}).status_code == 422
assert client.get("/convert", params={"from": "USD", "to": "GBP", "amount": "abc"}).status_code == 422
assert client.get(
    "/convert",
    params={"from": "USD", "to": "GBP", "amount": "1", "date": "2025-13-01"},
).status_code == 422
=== END AC convert-errors ===
