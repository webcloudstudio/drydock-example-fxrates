# FEATURE: Rates Latest

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Serve GET /rates/latest, returning every currency's rate on the most recent publication date. |
| Depends On | FEATURE-RatesByDate.md, FEATURE-EffectiveDate.md |
| Provides | GET /rates/latest |
| Consumes | rates.effective_publication |

## Purpose

`GET /rates/latest` returns the rates for the latest publication without the caller knowing its date.

## Routes

| Route | Behavior |
|-------|----------|
| `GET /rates/latest` | 200 with `{"date": <latest publication date>, "requested": "latest", "base": "EUR", "rates": {<code>: <rate>, ...}}`. 404 when the store holds no rates. |

## Behavior

- Register this route in the shared rates router in `app_server/routers/rates.py` ahead of
  `GET /rates/{date}`, so `latest` is never parsed as a date and rejected with 422.
- Resolve through `services.effective_date.effective_publication(db, None)`.

## Database Interface

- None — persistence is reached through `rates.effective_publication` in FEATURE-EffectiveDate.md.

## Programmatic Acceptance

=== AC rates-latest-returns-latest ===
Intent: The latest route returns the most recent publication, with requested set to the latest token, and is not shadowed by the dated route; a far-future seeded date is always the latest.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

latest = "9999-12-31"
earlier = "9999-12-30"
latest_rates = {"ZZA": "1.2300", "ZZB": "45.6"}
earlier_rates = {"ZZA": "7", "ZZC": "8"}

with db_session() as db:
    for cur, rate in latest_rates.items():
        db.rates.replace_rate(date=latest, currency=cur, rate=rate)
    for cur, rate in earlier_rates.items():
        db.rates.replace_rate(date=earlier, currency=cur, rate=rate)
    client = web_client()
    response = client.get("/rates/latest")
    assert response.status_code == 200
    body = response.json()
    assert body["date"] == latest
    assert body["requested"] == "latest"
    assert body["base"] == "EUR"
    assert body["rates"] == latest_rates
=== END AC rates-latest-returns-latest ===

=== AC rates-latest-matches-dated ===
Intent: The latest route and the dated route for the latest publication date return the same effective date and rates.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

latest = "9999-12-31"
rates_in = {"ZZA": "0.9430", "ZZB": "11.4555"}

with db_session() as db:
    for cur, rate in rates_in.items():
        db.rates.replace_rate(date=latest, currency=cur, rate=rate)
    client = web_client()
    by_latest = client.get("/rates/latest")
    assert by_latest.status_code == 200
    by_date = client.get(f"/rates/{latest}")
    assert by_date.status_code == 200
    a = by_latest.json()
    b = by_date.json()
    assert a["date"] == b["date"]
    assert a["rates"] == b["rates"]
    assert a["rates"] == rates_in
=== END AC rates-latest-matches-dated ===

## User Acceptance

- None.

## Guardrails

- `/rates/latest` is never answered with 422 as though `latest` were a malformed date.
- Rate values are the stored text as JSON strings.
