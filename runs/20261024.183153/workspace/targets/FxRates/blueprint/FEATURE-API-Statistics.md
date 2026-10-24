# FEATURE: API Statistics

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Reports stored-rate statistics and currencies available in the store. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /stats, GET /currencies |
| Consumes    | rates persistence operations |

## Purpose

Expose database-derived publication statistics and the set of currencies with at least one stored rate.

## Routes

### `GET /stats`

Return the number of distinct publication dates, total stored rates, and the earliest and latest stored dates. When no rates exist, the date bounds are `null`.

### `GET /currencies`

Return base currency EUR and all currencies with stored rates in ascending order.

## Data Access

Use the declared rates persistence operations. Derive counts, date bounds, and currency membership from stored records. Do not hardcode values.

## Programmatic Acceptance

=== AC stats-route ===
Intent: The statistics route is reachable and returns the declared response fields.

from app_server.testing import web_client

client = web_client()
response = client.get("/stats")
assert response.status_code == 200
body = response.json()
assert {"dates", "rates", "first", "last"} <= body.keys()
assert isinstance(body["dates"], int)
assert isinstance(body["rates"], int)
=== END AC stats-route ===

=== AC currencies-route ===
Intent: The currencies route is reachable and returns the declared base and currency collection fields.

from app_server.testing import web_client

client = web_client()
response = client.get("/currencies")
assert response.status_code == 200
body = response.json()
assert body["base"] == "EUR"
assert isinstance(body["currencies"], list)
assert body["currencies"] == sorted(body["currencies"])
=== END AC currencies-route ===

## User Acceptance

- None.

## Guardrails

- Counts, bounds, and currencies must come from the configured database through the persistence boundary.
- Currency codes are returned in ascending order.
