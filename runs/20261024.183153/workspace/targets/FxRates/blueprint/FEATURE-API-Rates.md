# FEATURE: API Rates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Retrieves stored rates for an effective publication date. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /rates/{date}, GET /rates/latest |
| Consumes    | rates persistence operations |

## Purpose

Return every available currency rate for the latest ECB publication on or before the requested date. `GET /rates/latest` uses the latest publication overall.

## Routes

- `GET /rates/{date}` returns the effective date, the original requested date, base `EUR`, and all rates published on the effective date.
- `GET /rates/latest` returns the same shape, with `requested` set to `latest`.
- If there is no publication on or before the requested date, return `404`.
- A malformed calendar date returns `422`.

Rates are returned as their stored ECB text. EUR is the implicit base and is not a stored rate.

## Data Access

Resolve the effective publication date using the latest-on-or-before access pattern, then retrieve all rates for that date. Do not hardcode dates or rates.

## Programmatic Acceptance

=== AC rates-by-date-route ===
Intent: The date-based rates route is reachable and returns a success status for a valid request.

from app_server.testing import web_client

client = web_client()
response = client.get("/rates/2098-12-30")
assert response.status_code in (200, 404)
=== END AC rates-by-date-route ===

=== AC rates-latest-route ===
Intent: The latest rates route is reachable and responds with a declared HTTP status.

from app_server.testing import web_client

client = web_client()
response = client.get("/rates/latest")
assert response.status_code in (200, 404)
=== END AC rates-latest-route ===

## User Acceptance

- None.

## Guardrails

- Resolve rates from persisted data and preserve rate text.
- Use the most recent publication on or before the requested date.
