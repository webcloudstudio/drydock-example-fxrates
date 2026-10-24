# FEATURE: Available Currencies

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Lists currencies with stored rates. |
| Depends On  | FEATURE-API-FOUNDATION.md, DATABASE.md |
| Provides    | GET /currencies |
| Consumes    | rates repository operations |

## Purpose

Return EUR as the base and currencies with at least one stored rate, sorted in ascending code order.

## Database Interface

- `FEATURE-DATA-005` — read: list stored currencies - supplies: `currency` - returns: `currency`

## Route

| Method | Path | Behavior |
|--------|------|----------|
| GET | `/currencies` | Returns the EUR base and distinct stored currency codes in ascending order. |

## Programmatic Acceptance

Requires: python-package=httpx; scope=test

=== AC currencies-route ===
Intent: The currencies route responds successfully with EUR as the declared base.

from app_server.testing import web_client

response = web_client().get("/currencies")
assert response.status_code == 200
body = response.json()
assert body["base"] == "EUR"
assert isinstance(body["currencies"], list)
=== END AC currencies-route ===

=== AC currencies-include-stored ===
Intent: The route includes a currency after a rate for it is stored.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-04-01"
currency = "TST"
rate = "1.2300"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)
    response = web_client().get("/currencies")
assert response.status_code == 200
assert currency in response.json()["currencies"]
=== END AC currencies-include-stored ===

=== AC currencies-sorted ===
Intent: The returned currency list is in ascending order.

from app_server.testing import web_client

response = web_client().get("/currencies")
assert response.status_code == 200
currencies = response.json()["currencies"]
assert currencies == sorted(currencies)
=== END AC currencies-sorted ===

## User Acceptance

- None.

## Guardrails

- Include only currencies with stored rates; EUR is the implicit base and need not have a stored rate.
