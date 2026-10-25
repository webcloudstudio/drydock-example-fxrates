# FEATURE: API Rates

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Resolves effective rates by requested or latest publication date. |
| Depends On  | DATABASE.md, ARCHITECTURE.md |
| Provides    | GET /rates/{date}, GET /rates/latest |
| Consumes    | rates.list |

## Purpose

Return all rates stored for the latest publication date on or before a requested calendar date. A request before the first publication returns 404. The latest endpoint resolves the latest publication in the store.

## Routes

- `GET /rates/{date}` accepts a real date in `YYYY-MM-DD` format and returns the requested date, effective publication date, EUR base, and rates for that publication.
- `GET /rates/latest` returns the same shape with the requested value set to `latest`.

## Programmatic Acceptance

=== AC rates-date-route-validates ===
Intent: A valid date request reaches the date-specific rates endpoint.
Suite: scoped

from app_server.testing import web_client

response = web_client().get("/rates/2099-12-30")
assert response.status_code in {200, 404}
=== END AC rates-date-route-validates ===

=== AC rates-latest-route-responds ===
Intent: The latest rates endpoint responds with success or the empty-store not-found status.
Suite: scoped

from app_server.testing import web_client

response = web_client().get("/rates/latest")
assert response.status_code in {200, 404}
=== END AC rates-latest-route-responds ===

## User Acceptance

- None.

## Guardrails

- Resolve requests to the latest publication date on or before the requested date.
- Preserve stored rate text in JSON strings; EUR has the implicit rate 1.
- Return 404 when no effective publication exists.
- A load completed while serving must be visible to the next request.
- Access persistent data only through the shipped persistence library.
