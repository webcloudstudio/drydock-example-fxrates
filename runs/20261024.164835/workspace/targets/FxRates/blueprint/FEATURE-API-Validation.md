# FEATURE: API Validation

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Enforces the API's malformed-input and unavailable-currency response statuses. |
| Depends On  | FEATURE-API-Foundation.md, FEATURE-API-Rates.md, FEATURE-API-Convert.md, FEATURE-API-History.md |
| Provides    | API request validation behavior |
| Consumes     | GET /rates/{date}, GET /convert, GET /history/{code} |

## Purpose

Ensure malformed dates and amounts and missing required query parameters return 422, and unknown or unavailable currencies return 404 on the applicable routes.

## Request rules

- A malformed date in a path or query returns 422.
- A malformed conversion amount returns 422.
- Missing required conversion parameters return 422.
- A conversion naming an unknown currency returns 404.
- A history request for a currency without stored rates returns 404.

## Programmatic Acceptance

=== AC validation-malformed-date ===
Intent: A malformed date on a provided route is refused with status 422.

from app_server.testing import web_client

client = web_client()
assert client.get("/rates/2025-13-01").status_code == 422
assert client.get("/history/GBP", params={"start": "2025-01-31-x"}).status_code == 422
=== END AC validation-malformed-date ===

=== AC validation-convert-parameters ===
Intent: Missing required conversion input and a malformed amount return status 422.

from app_server.testing import web_client

client = web_client()
assert client.get("/convert", params={"from": "USD", "to": "GBP"}).status_code == 422
assert client.get("/convert", params={"from": "USD", "to": "GBP", "amount": "abc"}).status_code == 422
=== END AC validation-convert-parameters ===

=== AC validation-unavailable-currencies ===
Intent: A conversion to an unavailable currency and history for an unstored currency return 404.

from persistence.testing import db_session
from app_server.testing import web_client

date = "2099-01-02"
with db_session() as db:
    db.rates.replace_rate(date=date, currency="USD", rate="1.1")

client = web_client()
assert client.get("/convert", params={"from": "USD", "to": "XXX", "amount": "1"}).status_code == 404
assert client.get("/history/HRK").status_code == 404
=== END AC validation-unavailable-currencies ===

## User Acceptance

- None.

## Guardrails

- Use the specified HTTP status codes; error response body wording is not part of this contract.
- Malformed dates and amounts and missing required query parameters return 422.
- Unknown or unavailable currencies return 404.
