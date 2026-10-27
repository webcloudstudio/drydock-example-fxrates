# FEATURE: Rates By Date

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Serve GET /rates/{date}, returning every currency's rate on the effective publication date. |
| Depends On | FEATURE-WebFoundation.md, FEATURE-EffectiveDate.md |
| Provides | GET /rates/{date} |
| Consumes | rates.effective_publication |

## Purpose

`GET /rates/{date}` answers what the euro reference rates were on a date, falling back to the latest
publication on or before it.

## Routes

| Route | Behavior |
|-------|----------|
| `GET /rates/{date}` | 200 with `{"date": <effective date>, "requested": <date>, "base": "EUR", "rates": {<code>: <rate>, ...}}`. Rates are the stored text as JSON strings. 404 when no publication is on or before the date. 422 when the path date is malformed. |

## Behavior

- The router lives in `app_server/routers/rates.py` and is included by `create_app()`. It uses the
  request-scoped database dependency from the web foundation.
- The path date must match `YYYY-MM-DD` and be a real calendar date; otherwise respond 422 through
  FastAPI request validation.
- The effective date and rates come from `services.effective_date.effective_publication`.

## Database Interface

- None — persistence is reached through `rates.effective_publication` in FEATURE-EffectiveDate.md.

## Programmatic Acceptance

=== AC rates-by-date-exact ===
Intent: A request for a publication date returns that date as both effective and requested, base EUR, and exactly that date's rates as stored text, excluding other dates.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

target = "1800-06-10"
other = "1800-06-09"
target_rates = {"ZZA": "1.0298", "ZZB": "160.2300", "ZZC": "0.84453"}
other_rates = {"ZZA": "5", "ZZD": "6"}

with db_session() as db:
    for cur, rate in target_rates.items():
        db.rates.replace_rate(date=target, currency=cur, rate=rate)
    for cur, rate in other_rates.items():
        db.rates.replace_rate(date=other, currency=cur, rate=rate)
    client = web_client()
    response = client.get(f"/rates/{target}")
    assert response.status_code == 200
    body = response.json()
    assert body["date"] == target
    assert body["requested"] == target
    assert body["base"] == "EUR"
    assert body["rates"] == target_rates
=== END AC rates-by-date-exact ===

=== AC rates-by-date-fallback ===
Intent: A non-publication date resolves to the latest earlier publication while echoing the requested date unchanged.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

published = "1800-06-15"
requested = "1800-06-17"
rates_in = {"ZZA": "2.5000", "ZZB": "10"}

with db_session() as db:
    for cur, rate in rates_in.items():
        db.rates.replace_rate(date=published, currency=cur, rate=rate)
    client = web_client()
    response = client.get(f"/rates/{requested}")
    assert response.status_code == 200
    body = response.json()
    assert body["date"] == published
    assert body["requested"] == requested
    assert body["rates"] == rates_in
=== END AC rates-by-date-fallback ===

=== AC rates-by-date-not-found ===
Intent: A date before every stored publication answers 404.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

with db_session() as db:
    db.rates.replace_rate(date="1800-06-20", currency="ZZA", rate="1")
    client = web_client()
    response = client.get("/rates/1799-01-01")
    assert response.status_code == 404
=== END AC rates-by-date-not-found ===

=== AC rates-by-date-malformed ===
Intent: A path date that is not a real YYYY-MM-DD calendar date is rejected with 422, never 404 or 500.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
for bad in ("2025-13-01", "2025-02-30", "not-a-date", "2025-1-5"):
    response = client.get(f"/rates/{bad}")
    assert response.status_code == 422, bad
=== END AC rates-by-date-malformed ===

## User Acceptance

- None.

## Guardrails

- Rate values are returned as the stored text in JSON strings, never as JSON numbers.
- The route does not query the database directly; it calls the effective-date service.
- Application startup never initializes the schema.
