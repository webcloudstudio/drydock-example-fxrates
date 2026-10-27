# FEATURE: Stats

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Serves GET /stats with the count of dates and rates and the first and last publication dates. |
| Depends On | FEATURE-WebFoundation.md, DATABASE.md |
| Provides | GET /stats |
| Consumes | db.rates.list_all |

## Purpose

Reports the size and span of the stored history, computed by the service from `db.rates.list_all`.

## Routes

| Route | Method | Status | Body |
|-------|--------|--------|------|
| `/stats` | GET | 200 | `{"dates": <n>, "rates": <n>, "first": <date>, "last": <date>}` |

| Field | Rule |
|-------|------|
| `dates` | Number of distinct dates with at least one stored rate. |
| `rates` | Number of stored rates. |
| `first` | Smallest stored date, `null` when the table is empty. |
| `last` | Largest stored date, `null` when the table is empty. |

## Database Interface

- `FEATURE-RATE-003` — read: list every stored rate - supplies: — - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC stats-counts-grow ===
Intent: After seeding three new dates with two currencies each, the dates count grows by three and the rates count by six relative to the counts read before setup.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

dates = ["1800-05-01", "1800-05-02", "1800-05-03"]
currencies = ["ZZA", "ZZB"]

client = web_client()
response = client.get("/stats")
assert response.status_code == 200
before = response.json()

with db_session() as db:
    for d in dates:
        for c in currencies:
            db.rates.replace_rate(date=d, currency=c, rate="1.5")
    response = client.get("/stats")
    assert response.status_code == 200
    after = response.json()

assert after["dates"] == before["dates"] + len(dates)
assert after["rates"] == before["rates"] + len(dates) * len(currencies)
=== END AC stats-counts-grow ===

=== AC stats-shape-and-span ===
Intent: The body has exactly the four declared keys, integer counts, and first and last that bound the seeded dates and equal the smallest and largest stored dates.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

seeded = ["1800-06-02", "1800-06-01"]

client = web_client()
with db_session() as db:
    for d in seeded:
        db.rates.replace_rate(date=d, currency="ZZA", rate="2.5")
    stored_dates = sorted({r.date for r in db.rates.list_all()})
    response = client.get("/stats")
    assert response.status_code == 200
    body = response.json()

assert set(body.keys()) == {"dates", "rates", "first", "last"}
assert isinstance(body["dates"], int)
assert isinstance(body["rates"], int)
assert body["dates"] == len(stored_dates)
assert body["first"] == stored_dates[0]
assert body["last"] == stored_dates[-1]
assert body["first"] <= min(seeded)
assert body["last"] >= max(seeded)
=== END AC stats-shape-and-span ===

=== AC stats-replace-not-double-counted ===
Intent: Storing the same date and currency twice adds one rate and one date, not two.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

date = "1800-07-01"
currency = "ZZA"

client = web_client()
before = client.get("/stats").json()
with db_session() as db:
    db.rates.replace_rate(date=date, currency=currency, rate="1.1")
    db.rates.replace_rate(date=date, currency=currency, rate="2.2")
    response = client.get("/stats")
    assert response.status_code == 200
    after = response.json()

assert after["dates"] == before["dates"] + 1
assert after["rates"] == before["rates"] + 1
=== END AC stats-replace-not-double-counted ===

## User Acceptance

- None.

## Guardrails

- Counts and spans are computed from stored rows on each request, never hardcoded or cached.
- Acceptance compares counts read before setup and never asserts absolute table counts.
- `first` and `last` are `null` when the table is empty.
