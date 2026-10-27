# FEATURE: Currency Listing

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Defines the API listing currencies with stored rates. |
| Depends On  | FEATURE-AppServer.md, DATABASE.md |
| Provides    | GET /currencies |
| Consumes    | create_app(), rates repository operations |

## Purpose

`GET /currencies` returns EUR as the base and the currencies with at least one stored rate, sorted in ascending order.

## Database Interface

- `FEATURE-RATE-005` — read: list stored rates - supplies: — - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC currencies-list-sorted ===
Intent: The endpoint lists currencies present in the store in ascending order.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-08-01"
currencies = ["QAZ", "QAA", "QAM"]

with db_session() as db:
    for index, currency in enumerate(currencies):
        db.rates.upsert(date=date, currency=currency, rate=str(index + 1))
    expected = sorted({row.currency for row in db.rates.list()})

client = web_client()
response = client.get("/currencies")
assert response.status_code == 200
body = response.json()
assert body["currencies"] == expected
assert body["currencies"] == sorted(body["currencies"])
assert all(currency in body["currencies"] for currency in currencies)
=== END AC currencies-list-sorted ===

=== AC currencies-base ===
Intent: The endpoint identifies EUR as the base currency.
Cite: sources/INSTRUCTIONS.md:59
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
response = client.get("/currencies")
assert response.status_code == 200
assert response.json()["base"] == "EUR"
=== END AC currencies-base ===

## User Acceptance

- None.

## Guardrails

- Include only currencies with at least one stored rate.
- Return currency codes in ascending order.
