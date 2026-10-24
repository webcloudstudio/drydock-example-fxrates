# FEATURE: API Request Validation

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Applies request validation statuses for malformed API input and unknown currencies. |
| Depends On  | FEATURE-Rates.md, FEATURE-Convert.md, FEATURE-History.md |
| Provides    | API request validation behavior |
| Consumes    | GET /rates/{date}, GET /convert, GET /history/{code} |

## Purpose

Malformed dates in a route or query, malformed conversion amounts, and missing required conversion parameters return 422. Unknown currencies return 404. Error response bodies are not part of this contract.

Validation applies to `/rates/{date}`, `/convert`, and `/history/{code}` date parameters. Conversion requires `from`, `to`, and `amount`.

## Programmatic Acceptance

=== AC malformed-date-is-unprocessable ===
Intent: A malformed requested rate date returns 422.

from app_server.testing import web_client

response = web_client().get("/rates/2098-13-01")
assert response.status_code == 422
=== END AC malformed-date-is-unprocessable ===

=== AC missing-conversion-amount-is-unprocessable ===
Intent: A conversion missing its required amount returns 422.

from app_server.testing import web_client

response = web_client().get("/convert", params={"from": "USD", "to": "GBP"})
assert response.status_code == 422
=== END AC missing-conversion-amount-is-unprocessable ===

=== AC malformed-amount-is-unprocessable ===
Intent: A malformed conversion amount returns 422.

from app_server.testing import web_client

response = web_client().get(
    "/convert", params={"from": "USD", "to": "GBP", "amount": "not-a-number"}
)
assert response.status_code == 422
=== END AC malformed-amount-is-unprocessable ===

=== AC unknown-currency-is-not-found ===
Intent: A conversion naming an unknown currency returns 404.

from persistence.testing import db_session
from app_server.testing import web_client

date = "2098-05-06"
currency = "ZZA"
rate = "1.5"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get(
    "/convert",
    params={"from": currency, "to": "ZZB", "amount": "1", "date": date},
)
assert response.status_code == 404
=== END AC unknown-currency-is-not-found ===

## User Acceptance

- None.

## Guardrails

- Error response bodies and diagnostic wording are not contractual.
- Use the declared HTTP status codes for validation and unknown-currency failures.
