# FEATURE: Currencies

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | List currencies that have at least one stored rate. |
| Depends On  | FEATURE-API-Foundation.md, DATABASE.md |
| Provides    | GET /currencies |
| Consumes    | rates repository operations |

## Purpose

`GET /currencies` returns the EUR base and the distinct currencies represented by at least one stored rate, in ascending order. EUR is implicit and is not included in the returned list unless it has a stored rate.

## Programmatic Acceptance

=== AC currencies-route ===
Intent: The currencies route is reachable and identifies EUR as the base.

from app_server.testing import web_client

response = web_client().get("/currencies")
assert response.status_code == 200
assert response.json()["base"] == "EUR"
assert isinstance(response.json()["currencies"], list)
=== END AC currencies-route ===

=== AC currencies-include-stored ===
Intent: A currency with a stored rate appears in the returned currency list.

from app_server.testing import web_client
from persistence.testing import committed_session

date = "2099-01-09"
currency = "ZZS"
rate = "9.012"

with committed_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

try:
    response = web_client().get("/currencies")
    assert response.status_code == 200
    currencies = response.json()["currencies"]
    assert currency in currencies
    assert currencies == sorted(currencies)
finally:
    with committed_session() as db:
        db.rates.delete(date=date, currency=currency)
=== END AC currencies-include-stored ===

## User Acceptance

- None.

## Guardrails

- List only currencies with at least one stored rate.
- Return currencies in ascending order.
- All database access goes through the generated persistence package.
