# FEATURE: History Empty

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | GET /history/{code} for a known currency with no points in range returns count 0, null statistics and no points. |
| Depends On | FEATURE-History.md |
| Provides | GET /history/{code} empty |
| Consumes | GET /history/{code} |

## Purpose

A currency with stored rates but none inside the requested period is a valid, empty answer rather than an error.

## Routes

| Route | Condition | Response |
|-------|-----------|----------|
| `GET /history/{code}` | The range holds no points for a currency with stored rates | 200 `{"currency", "base": "EUR", "count": 0, "min": null, "max": null, "mean": null, "points": []}` |

## Behavior

- No division is attempted on an empty set; `min`, `max` and `mean` are JSON `null`.
- The same applies when `start` is after `end`.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC history-empty-after-range ===
Intent: A start date after every stored point yields 200 with count 0, null statistics and an empty points list.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZE"
route = "/history/{code}"
with db_session() as db:
    db.rates.replace_rate(date="1800-07-01", currency=code, rate="1.5")
    client = web_client()
    resp = client.get(route.format(code=code), params={"start": "1800-08-01"})
    assert resp.status_code == 200
    body = resp.json()

assert body["currency"] == code
assert body["base"] == "EUR"
assert body["count"] == 0
assert body["min"] is None
assert body["max"] is None
assert body["mean"] is None
assert body["points"] == []
=== END AC history-empty-after-range ===

=== AC history-empty-before-range ===
Intent: An end date before every stored point yields the same empty answer, and a start later than end does too.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZF"
route = "/history/{code}"
cases = [
    {"end": "1800-06-01"},
    {"start": "1800-09-02", "end": "1800-09-01"},
]
with db_session() as db:
    db.rates.replace_rate(date="1800-09-01", currency=code, rate="2.5")
    db.rates.replace_rate(date="1800-09-03", currency=code, rate="3.5")
    client = web_client()
    for params in cases:
        resp = client.get(route.format(code=code), params=params)
        assert resp.status_code == 200, params
        body = resp.json()
        assert body["count"] == 0, params
        assert body["min"] is None and body["max"] is None and body["mean"] is None, params
        assert body["points"] == [], params
=== END AC history-empty-before-range ===

=== AC history-empty-then-populated ===
Intent: The same currency returns an empty answer for a range outside its data and a non-empty answer for a range covering it, so the empty case is range-driven.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZG"
date, rate = "1800-12-05", "4.25"
route = "/history/{code}"
with db_session() as db:
    db.rates.replace_rate(date=date, currency=code, rate=rate)
    client = web_client()
    empty = client.get(route.format(code=code), params={"start": "1800-12-06"})
    assert empty.status_code == 200
    assert empty.json()["count"] == 0
    full = client.get(route.format(code=code), params={"start": date, "end": date})
    assert full.status_code == 200
    body = full.json()
    assert body["count"] == 1
    assert body["points"] == [{"date": date, "rate": rate}]
    assert body["min"] == rate and body["max"] == rate
=== END AC history-empty-then-populated ===

## User Acceptance

- None.

## Guardrails

- Empty results never produce 404 or a numeric zero for `min`, `max` or `mean`.
- No floating point is introduced for the empty case.
