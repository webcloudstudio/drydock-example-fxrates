# FEATURE: Rates Latest

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | GET /rates/latest returns the rates of the latest publication date with requested set to "latest". |
| Depends On | FEATURE-RatesByDate.md, DATABASE.md |
| Provides | GET /rates/latest |
| Consumes | GET /rates/{date}, rates repository operations |

## Purpose

Serve the most recent publication without the caller knowing its date.

## Behavior

- `GET /rates/latest` finds the latest publication date overall with `rates.list_on_or_before` called without `as_of`; the first row is the latest date.
- The 200 body has the same shape as `/rates/{date}`: `date`, `requested`, `base` "EUR", and `rates` mapping each stored currency to its stored rate text. `requested` is the string `"latest"`.
- When nothing is stored the response is 404.
- The route is registered before `/rates/{date}` so `latest` is never parsed as a malformed date (which would yield 422).

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC latest-body ===
Intent: With a seeded publication later than any real one, /rates/latest returns that date, requested "latest", base EUR, and exactly the seeded rate texts.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

older = "2999-01-01"
newest = "2999-01-05"
rates = {"ZZA": "1.2500", "ZZB": "0.943"}

with db_session() as db:
    db.rates.replace_rate(date=older, currency="ZZA", rate="9.9")
    for code, text in rates.items():
        db.rates.replace_rate(date=newest, currency=code, rate=text)
    client = web_client()
    response = client.get("/rates/latest")
    assert response.status_code == 200
    body = response.json()
    assert body["date"] == newest
    assert body["requested"] == "latest"
    assert body["base"] == "EUR"
    assert body["rates"] == rates
=== END AC latest-body ===

=== AC latest-not-parsed-as-date ===
Intent: The literal path segment latest is routed to the latest handler and never rejected as a malformed date (422).
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

d = "2999-02-01"

with db_session() as db:
    db.rates.replace_rate(date=d, currency="ZZA", rate="3")
    client = web_client()
    response = client.get("/rates/latest")
    assert response.status_code == 200
    bad = client.get("/rates/not-a-date")
    assert bad.status_code == 422
=== END AC latest-not-parsed-as-date ===

=== AC latest-matches-by-date ===
Intent: /rates/latest and /rates/{date} for the latest date return identical rates and date, differing only in requested.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

d = "2999-03-01"

with db_session() as db:
    db.rates.replace_rate(date=d, currency="ZZA", rate="4.5")
    db.rates.replace_rate(date=d, currency="ZZB", rate="5.25")
    client = web_client()
    latest = client.get("/rates/latest")
    assert latest.status_code == 200
    dated = client.get("/rates/" + d)
    assert dated.status_code == 200
    a = latest.json()
    b = dated.json()
    assert a["date"] == b["date"]
    assert a["rates"] == b["rates"]
    assert a["requested"] == "latest"
    assert b["requested"] == d
=== END AC latest-matches-by-date ===

## User Acceptance

- None.

## Guardrails

- Rates are returned as the stored text, never as floating point.
- No rate, date, or count is hardcoded; every value comes from a query.
- `/rates/latest` must be registered before `/rates/{date}`.
