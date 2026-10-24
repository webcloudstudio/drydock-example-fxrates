# FEATURE: List Currencies

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Lists EUR and currencies with stored rates in ascending order. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /currencies |
| Consumes    | rates.list |

## Purpose

Return the EUR base and every currency with at least one stored rate, sorted by currency code in ascending order.

## Routes

| Method | Path | Behavior |
|--------|------|----------|
| GET | `/currencies` | Return the EUR base and the ascending list of currencies with stored rates. |

## Database Interface

- `FEATURE-RATE-002` — read: list rates for a publication date - supplies: `date` - returns: `date`, `currency`, `rate`

The repository operation supports listing by publication date, not all currencies. The implementation may derive the currency set from persisted data through the declared interface only; it must not open SQLite directly or introduce an undeclared query.

## Programmatic Acceptance

=== AC currencies-route ===
Intent: The currencies route returns a successful JSON response with the EUR base and currency codes.

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    db.rates.upsert(date="2001-04-01", currency="USD", rate="1.2")
    db.rates.upsert(date="2001-04-01", currency="JPY", rate="130")

response = web_client().get("/currencies")
assert response.status_code == 200
body = response.json()
assert body["base"] == "EUR"
assert "currencies" in body
assert isinstance(body["currencies"], list)
assert len(body["currencies"]) >= 2
=== END AC currencies-route ===
