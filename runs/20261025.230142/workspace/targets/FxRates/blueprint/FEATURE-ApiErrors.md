# FEATURE: API Errors

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Validate API requests and return the specified error statuses. |
| Depends On  | FEATURE-EffectiveRates.md, FEATURE-Convert.md, FEATURE-CurrencyHistory.md |
| Provides    | API request validation and error responses |
| Consumes    | GET /rates/{date}, GET /convert, GET /history/{code} |

## Purpose

Keep request validation and error behavior consistent across the rates, conversion, and history endpoints.

## Behavior

- A malformed date in a path or query, malformed conversion amount, or missing required query parameter returns HTTP 422.
- A requested date with no publication on or before it returns HTTP 404.
- A conversion naming a non-EUR currency with no rate on the effective date returns HTTP 404.
- A history request for a currency with no stored rate, including EUR when no EUR rate is stored, returns HTTP 404.
- FastAPI request validation supplies 422 responses.

## Programmatic Acceptance

=== AC malformed_rate_date ===
Intent: A malformed date path parameter is rejected with status 422.
Requires: python-package=httpx; scope=test

from app_server.testing import web_client

client = web_client()
response = client.get("/rates/2025-13-01")
assert response.status_code == 422
=== END AC malformed_rate_date ===

=== AC missing_convert_amount ===
Intent: A conversion request missing its required amount is rejected with status 422.
Requires: python-package=httpx; scope=test

from app_server.testing import web_client

client = web_client()
response = client.get("/convert", params={"from": "USD", "to": "GBP"})
assert response.status_code == 422
=== END AC missing_convert_amount ===

=== AC malformed_convert_amount ===
Intent: A malformed conversion amount is rejected with status 422.
Requires: python-package=httpx; scope=test

from app_server.testing import web_client

client = web_client()
response = client.get("/convert", params={"from": "USD", "to": "GBP", "amount": "abc"})
assert response.status_code == 422
=== END AC malformed_convert_amount ===

=== AC missing_effective_publication ===
Intent: A date before every available publication has no effective rate response.
Requires: python-package=httpx; scope=test

from app_server.testing import web_client

client = web_client()
response = client.get("/rates/1900-01-01")
assert response.status_code == 404
=== END AC missing_effective_publication ===

=== AC unavailable_conversion_currency ===
Intent: A conversion whose target currency has no rate on the effective date returns not found.
Requires: python-package=httpx; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

date = "2098-01-02"
source_currency = "ZZZ"
target_currency = "YYY"
amount = "1"

with db_session() as db:
    db.rates.upsert(date=date, currency=source_currency, rate="2")

client = web_client()
response = client.get(
    "/convert",
    params={"from": source_currency, "to": target_currency, "amount": amount, "date": date},
)
assert response.status_code == 404
=== END AC unavailable_conversion_currency ===

=== AC currency_without_history ===
Intent: A currency with no stored rates has no history response.
Requires: python-package=httpx; scope=test

from app_server.testing import web_client

currency = "ZZZ"
client = web_client()
response = client.get(f"/history/{currency}")
assert response.status_code == 404
=== END AC currency_without_history ===

## User Acceptance

- None.

## Guardrails

- Invalid request status codes follow the specified API contract.
- Error response bodies are not part of the response contract.
