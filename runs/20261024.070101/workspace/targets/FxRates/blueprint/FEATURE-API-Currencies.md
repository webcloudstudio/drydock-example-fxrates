# FEATURE: API Currencies

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Lists currencies that have at least one stored rate. |
| Depends On  | DATABASE.md |
| Provides    | GET /currencies |
| Consumes    | rates repository operations |

## Route

### GET /currencies

Returns JSON with base `"EUR"` and currencies having at least one stored rate, sorted in ascending order. EUR is the implicit base and is not included unless it has a stored rate.

## Database Interface

- `FEATURE-RATE-002` — read: list rates with optional equality filters - supplies: `date`, `currency` - returns: `id`, `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC currencies-route ===
Intent: The currency listing route returns success and sorted codes from stored rates.

from persistence.testing import db_session
from app_server.testing import web_client

with db_session() as db:
    db.rates.upsert(date="2099-01-02", currency="ZZZ", rate="1.25")
    db.rates.upsert(date="2099-01-02", currency="AAA", rate="2.50")

response = web_client().get("/currencies")
assert response.status_code == 200
body = response.json()
assert body["base"] == "EUR"
assert body["currencies"] == sorted(body["currencies"])
assert "AAA" in body["currencies"]
assert "ZZZ" in body["currencies"]
=== END AC currencies-route ===

## User Acceptance

- None.

## Guardrails

- Derive currencies from stored rates.
- Return currencies in ascending order.
- Do not hardcode the available currency list.
