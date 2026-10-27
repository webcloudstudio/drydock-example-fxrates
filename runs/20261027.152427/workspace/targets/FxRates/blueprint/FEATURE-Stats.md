# FEATURE: Stats

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | `GET /stats` reports the number of stored dates and rates and the first and last publication dates. |
| Depends On | FEATURE-ServeHealth.md, FEATURE-LoadStore.md |
| Provides | GET /stats |
| Consumes | rates.list_all_keys, app_server.create_app |

## Purpose

Give a summary of what the store holds.

## Route

`GET /stats` returns status 200 with `{"dates": <n>, "rates": <n>, "first": <date>, "last": <date>}`.

- `dates` is the number of distinct publication dates with a stored rate.
- `rates` is the number of stored rates.
- `first` and `last` are the earliest and latest stored dates, and are `null` when nothing is stored.
- `dates` and `rates` are JSON integers.

Every value is computed from `rates.list_all_keys` called without `since`; the service counts and
takes the first and last date. Nothing is hardcoded.

## Database Interface

- `FEATURE-RATE-004` — read: list every stored date and currency - supplies: — - returns: `date`, `currency`

## Programmatic Acceptance

=== AC stats-reflects-store ===
Intent: The stats body equals the counts, first date and last date derived from the stored keys read back through the repository, and includes the rows the criterion seeded.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

d1 = "1900-09-01"
d2 = "1900-09-02"

with db_session() as db:
    db.rates.replace_rate(date=d1, currency="ZZA", rate="1.1")
    db.rates.replace_rate(date=d1, currency="ZZB", rate="2.2")
    db.rates.replace_rate(date=d2, currency="ZZA", rate="1.2")
    keys = db.rates.list_all_keys()
    dates = sorted({k.date for k in keys})
    client = web_client()
    response = client.get("/stats")
    assert response.status_code == 200
    body = response.json()
    assert body["dates"] == len(dates)
    assert body["rates"] == len(keys)
    assert body["first"] == dates[0]
    assert body["last"] == dates[-1]
    assert isinstance(body["dates"], int)
    assert isinstance(body["rates"], int)
    assert body["first"] <= d1
    assert body["last"] >= d2
=== END AC stats-reflects-store ===

=== AC stats-body-shape ===
Intent: The stats body carries exactly the four declared keys, and first and last are null exactly when no rate is stored.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    keys = db.rates.list_all_keys()
    client = web_client()
    response = client.get("/stats")
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"dates", "rates", "first", "last"}
    if not keys:
        assert body["dates"] == 0
        assert body["rates"] == 0
        assert body["first"] is None
        assert body["last"] is None
    else:
        assert isinstance(body["first"], str)
        assert isinstance(body["last"], str)
=== END AC stats-body-shape ===

## User Acceptance

- None.

## Guardrails

- No count, date, or total is hardcoded; every value comes from a query.
- The route reaches the store only through the generated persistence package.
