# FEATURE: Currencies

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | `GET /currencies` lists the base currency and every currency with a stored rate, ascending. |
| Depends On | FEATURE-ServeHealth.md, FEATURE-LoadStore.md |
| Provides | GET /currencies |
| Consumes | rates.list_currencies, app_server.create_app |

## Purpose

Tell a caller which currency codes the service can quote.

## Route

`GET /currencies` returns status 200 with `{"base": "EUR", "currencies": [<code>, ...]}`.

- `currencies` holds each currency with at least one stored rate, once, in ascending order.
- EUR is the base and is not listed among the currencies.
- When no rate is stored, `currencies` is the empty list and `base` is still `EUR`.

The service calls `rates.list_currencies` without `since` and removes duplicates.

## Database Interface

- `FEATURE-RATE-005` — read: list stored currency codes - supplies: — - returns: `currency`

## Programmatic Acceptance

=== AC currencies-lists-stored ===
Intent: The currency list equals the distinct stored codes read back through the repository, ascending, includes the seeded codes, and omits EUR.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

d = "1900-11-01"
seeded = ["ZZC", "ZZA", "ZZB"]

with db_session() as db:
    for i, code in enumerate(seeded):
        db.rates.replace_rate(date=d, currency=code, rate=str(i + 1))
    expected = sorted({r.currency for r in db.rates.list_currencies()})
    client = web_client()
    response = client.get("/currencies")
    assert response.status_code == 200
    body = response.json()
    assert body["base"] == "EUR"
    assert body["currencies"] == expected
    assert body["currencies"] == sorted(set(body["currencies"]))
    for code in seeded:
        assert code in body["currencies"]
    assert "EUR" not in body["currencies"]
=== END AC currencies-lists-stored ===

=== AC currencies-body-shape ===
Intent: The body carries exactly base and currencies, currencies is a list, and it is empty exactly when no rate is stored.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    stored = db.rates.list_currencies()
    client = web_client()
    response = client.get("/currencies")
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"base", "currencies"}
    assert isinstance(body["currencies"], list)
    if not stored:
        assert body["currencies"] == []
    else:
        assert len(body["currencies"]) >= 1
=== END AC currencies-body-shape ===

## User Acceptance

- None.

## Guardrails

- No currency code is hardcoded; the list comes from a query.
- The route reaches the store only through the generated persistence package.
