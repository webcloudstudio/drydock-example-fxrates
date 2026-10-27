# FEATURE: Rates By Date

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | `GET /rates/{date}` resolves the effective publication date and lists the rates published on it. |
| Depends On | FEATURE-ServeHealth.md, FEATURE-LoadStore.md |
| Provides | GET /rates/{date}, fxrates_app.rates.effective_date |
| Consumes | rates.list_on_or_before, rates.list_for_date, app_server.create_app |

## Purpose

Answer which rates applied on a calendar day. The ECB publishes on working days only, so a request
for any date uses the latest publication on or before it.

## Effective date

`fxrates_app.rates.effective_date(d)` returns the latest publication date on or before `d`, or
`None` when no such date exists. It is computed with `rates.list_on_or_before(as_of=d)`; the first
row's date is the effective date. Other stories (`/convert`, `/history`, `/rates/latest`) reuse it.

## Route

`GET /rates/{date}`:

| Condition | Status | Body |
|-----------|--------|------|
| `date` is a real calendar date `YYYY-MM-DD` with an effective date | 200 | `{"date": <effective>, "requested": <date>, "base": "EUR", "rates": {<code>: <stored text>, ...}}` |
| `date` is a real date with no publication on or before it | 404 | any |
| `date` is malformed or not a real date (for example `2025-13-01`) | 422 | any |

- `rates` holds every currency with a rate on the effective date, as the stored text in a JSON
  string, and has no `EUR` entry.
- The date is validated through FastAPI request validation, which produces 422.
- Static routes such as `/rates/latest` are registered before this dynamic route so `latest` is not
  parsed as a date.

## Database Interface

- `FEATURE-RATE-003` — read: list publication dates on or before a date - supplies: `as_of` - returns: `date`
- `FEATURE-RATE-002` — read: list every rate published on one date - supplies: `date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC rates-by-date-exact ===
Intent: A request for a publication date returns that date as both date and requested, base EUR, and each stored rate text exactly as supplied.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

d = "1900-10-01"
ra = "1.50"
rb = "2.250"

with db_session() as db:
    db.rates.replace_rate(date=d, currency="ZZA", rate=ra)
    db.rates.replace_rate(date=d, currency="ZZB", rate=rb)
    client = web_client()
    response = client.get(f"/rates/{d}")
    assert response.status_code == 200
    body = response.json()
    assert body["date"] == d
    assert body["requested"] == d
    assert body["base"] == "EUR"
    assert body["rates"]["ZZA"] == ra
    assert body["rates"]["ZZB"] == rb
    assert "EUR" not in body["rates"]
    stored = {r.currency: r.rate for r in db.rates.list_for_date(date=d)}
    assert body["rates"] == stored
=== END AC rates-by-date-exact ===

=== AC rates-by-date-effective ===
Intent: A request between two publications resolves to the earlier publication, keeps the requested date, and carries that earlier date's rates rather than the later ones.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

early = "1900-10-01"
late = "1900-10-05"
between = "1900-10-03"
r_early = "1.50"
r_late = "1.6"

with db_session() as db:
    db.rates.replace_rate(date=early, currency="ZZA", rate=r_early)
    db.rates.replace_rate(date=late, currency="ZZA", rate=r_late)
    client = web_client()
    response = client.get(f"/rates/{between}")
    assert response.status_code == 200
    body = response.json()
    assert body["date"] == early
    assert body["requested"] == between
    assert body["rates"]["ZZA"] == r_early
=== END AC rates-by-date-effective ===

=== AC rates-effective-date-function ===
Intent: effective_date returns the latest publication date on or before its argument and None when none exists.
Requires: executable=python3; scope=test

from fxrates_app.rates import effective_date
from persistence.testing import db_session

early = "1900-10-01"
late = "1900-10-05"
between = "1900-10-03"
before_all = "1899-12-31"

with db_session() as db:
    db.rates.replace_rate(date=early, currency="ZZA", rate="1")
    db.rates.replace_rate(date=late, currency="ZZA", rate="2")
    assert effective_date(between) == early
    assert effective_date(late) == late
    assert effective_date(before_all) is None
=== END AC rates-effective-date-function ===

=== AC rates-by-date-errors ===
Intent: A date before every publication answers 404, and malformed or impossible dates answer 422.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
before_all = "1899-12-31"
assert client.get(f"/rates/{before_all}").status_code == 404
assert client.get("/rates/2025-13-01").status_code == 422
assert client.get("/rates/not-a-date").status_code == 422
assert client.get("/rates/2025-01-31-x").status_code == 422
=== END AC rates-by-date-errors ===

## User Acceptance

- None.

## Guardrails

- No rate or date is hardcoded; every value comes from a query.
- Rates are returned as the stored text, never converted to a float.
- EUR never appears in the `rates` map.
