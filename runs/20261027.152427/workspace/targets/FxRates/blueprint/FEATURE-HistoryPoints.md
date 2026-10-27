# FEATURE: History Points

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | GET /history/{code} lists a currency's stored rates in ascending date order between optional inclusive bounds. |
| Depends On | ARCHITECTURE.md, DATABASE.md, FEATURE-RatesByDate.md, FEATURE-WebFoundation.md |
| Provides | GET /history/{code} |
| Consumes | fxrates_app.rates.effective_date, rates repository operations, app_server.create_app |

## Purpose

Serve a currency's history over a period. The response is a JSON object with `currency`, `base`
(always `EUR`), `count`, `min`, `max`, `mean`, and `points`. This story delivers `currency`, `base`,
and `points`; the statistics fields are specified by `FEATURE-HistoryStats.md` and implemented
over the same route.

## Route

`GET /history/{code}` with optional query parameters `start` and `end`, each a calendar date
`YYYY-MM-DD`.

## Behavior

- `points` holds one `{"date": <date>, "rate": <stored text>}` object per publication date of the
  currency from `start` through `end` inclusive, in ascending date order.
- Both bounds are optional. Without `start` the history begins at the earliest stored date; without
  `end` it runs to the latest.
- Each `rate` is the stored text as a JSON string, exactly as the ECB published it (`0.943` stays
  `0.943`). No arithmetic or float conversion is applied to a point.
- When `start` is later than `end`, the response is 200 with an empty `points` list.
- A currency code is matched as given; the response `currency` echoes it.
- A history is read through the persistence library by one call per request, so a load completed
  before the request is visible to it.

## Database Interface

- `FEATURE-RATE-006` — read: list a currency's rates over a period - supplies: `currency`, `start_date`, `end_date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC history-points-range ===
Intent: Points between inclusive bounds come back ascending with the stored rate text, derived from the seeded inputs by sorting on date.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZH"
rates = {
    "1900-08-03": "1.50",
    "1900-08-01": "1.0316",
    "1900-08-02": "2",
    "1900-08-04": "0.943",
}
start = "1900-08-02"
end = "1900-08-03"

with db_session() as db:
    for d, r in rates.items():
        db.rates.replace_rate(date=d, currency=code, rate=r)
    client = web_client()
    resp = client.get(f"/history/{code}", params={"start": start, "end": end})
    assert resp.status_code == 200
    body = resp.json()
    expected = [{"date": d, "rate": rates[d]} for d in sorted(rates) if start <= d <= end]
    assert body["points"] == expected
    assert body["currency"] == code
    assert body["count"] == len(expected)
=== END AC history-points-range ===

=== AC history-points-optional-bounds ===
Intent: Each bound is optional on its own; omitting both returns every stored point, and text such as 0.943 is returned exactly as stored.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZH"
rates = {
    "1900-09-04": "0.943",
    "1900-09-02": "1.50",
    "1900-09-03": "1.0316",
    "1900-09-01": "7",
}
cut = "1900-09-03"

with db_session() as db:
    for d, r in rates.items():
        db.rates.replace_rate(date=d, currency=code, rate=r)
    client = web_client()

    resp = client.get(f"/history/{code}")
    assert resp.status_code == 200
    assert resp.json()["points"] == [{"date": d, "rate": rates[d]} for d in sorted(rates)]

    resp = client.get(f"/history/{code}", params={"start": cut})
    assert resp.status_code == 200
    assert resp.json()["points"] == [
        {"date": d, "rate": rates[d]} for d in sorted(rates) if d >= cut
    ]

    resp = client.get(f"/history/{code}", params={"end": cut})
    assert resp.status_code == 200
    assert resp.json()["points"] == [
        {"date": d, "rate": rates[d]} for d in sorted(rates) if d <= cut
    ]
=== END AC history-points-optional-bounds ===

=== AC history-points-start-after-end ===
Intent: A start later than end is not an error; the response is 200 with no points even though the currency has stored rates.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZH"
dates = ["1900-10-01", "1900-10-02", "1900-10-03"]
start = "1900-10-03"
end = "1900-10-01"

with db_session() as db:
    for d in dates:
        db.rates.replace_rate(date=d, currency=code, rate="3")
    client = web_client()
    resp = client.get(f"/history/{code}", params={"start": start, "end": end})
    assert resp.status_code == 200
    body = resp.json()
    assert body["points"] == []
    assert body["count"] == 0
=== END AC history-points-start-after-end ===

=== AC history-points-round-trip ===
Intent: A replaced rate is what the next request returns, proving history is read from the store on each request and holds one point per date.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZH"
d = "1900-11-01"
first = "1.25"
second = "1.75"

with db_session() as db:
    db.rates.replace_rate(date=d, currency=code, rate=first)
    client = web_client()
    resp = client.get(f"/history/{code}")
    assert resp.status_code == 200
    assert resp.json()["points"] == [{"date": d, "rate": first}]

    db.rates.replace_rate(date=d, currency=code, rate=second)
    resp = client.get(f"/history/{code}")
    assert resp.status_code == 200
    assert resp.json()["points"] == [{"date": d, "rate": second}]
=== END AC history-points-round-trip ===

## User Acceptance

- None.

## Guardrails

- Rates are returned as stored text and never converted to floating point.
- No rate, date, or count is hardcoded; every value comes from a repository query.
- Application code reaches the store only through the shipped persistence library.
