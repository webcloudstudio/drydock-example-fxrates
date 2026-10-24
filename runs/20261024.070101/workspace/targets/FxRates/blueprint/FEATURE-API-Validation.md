# FEATURE: API Request Validation

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Enforces request validation and not-found responses across rate API requests. |
| Depends On  | FEATURE-API-Rates.md, FEATURE-API-Convert.md, FEATURE-API-History.md |
| Provides    | API request validation behavior |
| Consumes    | GET /rates/{date}, GET /convert, GET /history/{code} |

## Purpose

Ensure malformed dates in path and query parameters, malformed conversion amounts, and missing required conversion parameters receive HTTP 422. Unknown currencies, currencies without a required rate, unknown history currencies, and dates without any prior publication receive HTTP 404. This specification owns validation and error-status behavior for the rates, conversion, and history routes.

## Programmatic Acceptance

Requires: python-package=httpx; scope=test

=== AC validation-date-path ===
Intent: A malformed date in the rates path receives request-validation status.

from app_server.testing import web_client

response = web_client().get("/rates/2099-13-01")
assert response.status_code == 422
=== END AC validation-date-path ===

=== AC validation-convert-missing-parameter ===
Intent: A missing required conversion parameter receives request-validation status.

from app_server.testing import web_client

response = web_client().get("/convert", params={"from": "EUR", "to": "EUR"})
assert response.status_code == 422
=== END AC validation-convert-missing-parameter ===

=== AC validation-unknown-conversion-currency ===
Intent: A conversion naming a currency without a rate receives not found.

from persistence.testing import db_session
from app_server.testing import web_client

publication = "2099-01-02"
currency = "AAA"
with db_session() as db:
    db.rates.upsert(date=publication, currency=currency, rate="1.23")

response = web_client().get(
    "/convert",
    params={"from": currency, "to": "ZZZ", "amount": "1", "date": publication},
)
assert response.status_code == 404
=== END AC validation-unknown-conversion-currency ===

=== AC validation-history-currency ===
Intent: A history request for a currency with no stored rate receives not found.

from app_server.testing import web_client

response = web_client().get("/history/ZZZ")
assert response.status_code == 404
=== END AC validation-history-currency ===

## User Acceptance

- None.

## Guardrails

- Use HTTP 422 for malformed dates or amounts and missing required conversion parameters.
- Use HTTP 404 for unknown currencies and unavailable rates.
- Error response body wording is not part of the response contract.
