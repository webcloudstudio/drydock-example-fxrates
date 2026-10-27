# FEATURE: Currencies

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Serves GET /currencies listing every currency with at least one stored rate in ascending order. |
| Depends On | FEATURE-WebFoundation.md, DATABASE.md |
| Provides | GET /currencies |
| Consumes | db.rates.list_all |

## Purpose

Lists the currencies the store can answer for, with EUR as the stated base.

## Routes

| Route | Method | Status | Body |
|-------|--------|--------|------|
| `/currencies` | GET | 200 | `{"base": "EUR", "currencies": [<code>, ...]}` |

`currencies` holds every currency with at least one stored rate, each once, in ascending code order. EUR appears only if a rate is stored for it.

## Database Interface

- `FEATURE-RATE-003` — read: list every stored rate - supplies: — - returns: `currency`

## Programmatic Acceptance

=== AC currencies-ascending-distinct ===
Intent: Seeded currencies inserted out of order on several dates appear exactly once each in the ascending list, and the list equals the sorted distinct currencies read from the store.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

seeded = ["ZZC", "ZZA", "ZZB"]
dates = ["1800-08-01", "1800-08-02"]

client = web_client()
with db_session() as db:
    for d in dates:
        for c in seeded:
            db.rates.replace_rate(date=d, currency=c, rate="3.5")
    expected = sorted({r.currency for r in db.rates.list_all()})
    response = client.get("/currencies")
    assert response.status_code == 200
    body = response.json()

assert body["base"] == "EUR"
assert body["currencies"] == expected
for c in seeded:
    assert body["currencies"].count(c) == 1
=== END AC currencies-ascending-distinct ===

=== AC currencies-shape ===
Intent: The body has exactly the keys base and currencies, and currencies is a list of strings.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

client = web_client()
with db_session() as db:
    db.rates.replace_rate(date="1800-09-01", currency="ZZA", rate="1.0")
    response = client.get("/currencies")
    assert response.status_code == 200
    body = response.json()

assert set(body.keys()) == {"base", "currencies"}
assert isinstance(body["currencies"], list)
assert all(isinstance(c, str) for c in body["currencies"])
assert body["currencies"] == sorted(body["currencies"])
=== END AC currencies-shape ===

=== AC currencies-new-currency-appears ===
Intent: A currency with no stored rate is absent, and it appears after a rate for it is stored.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

currency = "ZZQ"

client = web_client()
with db_session() as db:
    before = client.get("/currencies")
    assert before.status_code == 200
    assert currency not in before.json()["currencies"]
    db.rates.replace_rate(date="1800-10-01", currency=currency, rate="4.0")
    after = client.get("/currencies")
    assert after.status_code == 200
    assert currency in after.json()["currencies"]
=== END AC currencies-new-currency-appears ===

## User Acceptance

- None.

## Guardrails

- The list is computed from stored rows on each request, never hardcoded.
- A currency whose only rates are `N/A` is never stored and so never listed.
