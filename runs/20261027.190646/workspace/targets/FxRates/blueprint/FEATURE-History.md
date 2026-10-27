# FEATURE: History

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | GET /history/{code} returns a currency's rates over a period with exact minimum, maximum and mean. |
| Depends On | DATABASE.md, FEATURE-WebFoundation.md |
| Provides | GET /history/{code} |
| Consumes | db.rates.history |

## Purpose

Report one currency's stored rates between optional inclusive `start` and `end` dates, with statistics computed exactly from the stored text.

## Routes

| Route | Response 200 |
|-------|--------------|
| `GET /history/{code}[?start=<date>][&end=<date>]` | `{"currency", "base": "EUR", "count", "min", "max", "mean", "points": [{"date", "rate"}, ...]}` |

## Behavior

- Points come from `db.rates.history` ascending by date; both bounds are inclusive and optional.
- `count` is the number of points.
- `min` and `max` are the stored text of the smallest and largest rate by `Decimal` value, not by string order.
- `mean` is the exact `Decimal` mean of the point rates, rounded half to even to six decimals and written with exactly six decimals, as a JSON string.
- Point `rate` values are the stored text as JSON strings.
- Empty ranges and unknown currencies are owned by later stories (FEATURE-HistoryEmpty.md, FEATURE-HistoryRejects.md).

## Database Interface

- `FEATURE-RATE-004` — read: list a currency's history over a period - supplies: `currency`, `start_date`, `end_date` - returns: `date`, `rate`

## Programmatic Acceptance

=== AC history-statistics ===
Intent: History returns points ascending, stored text for min and max chosen by decimal value (10.5 beats 9.75 though it sorts lower as a string), and the exact half-even mean.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZH"
points = [("1800-04-03", "10.5"), ("1800-04-01", "9.75"), ("1800-04-02", "9.8")]
route = "/history/{code}"
with db_session() as db:
    for date, rate in points:
        db.rates.replace_rate(date=date, currency=code, rate=rate)
    client = web_client()
    resp = client.get(route.format(code=code))
    assert resp.status_code == 200
    body = resp.json()

ordered = sorted(points, key=lambda p: p[0])
values = [Decimal(r) for _, r in points]
min_text = min(points, key=lambda p: Decimal(p[1]))[1]
max_text = max(points, key=lambda p: Decimal(p[1]))[1]
mean = (sum(values) / len(values)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)

assert body["currency"] == code
assert body["base"] == "EUR"
assert body["count"] == len(points)
assert body["min"] == min_text
assert body["max"] == max_text
assert body["mean"] == f"{mean:.6f}"
assert body["points"] == [{"date": d, "rate": r} for d, r in ordered]
=== END AC history-statistics ===

=== AC history-bounds-inclusive ===
Intent: Optional start and end bounds are inclusive, can be used alone or together, and statistics cover only the selected points.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZB"
points = [
    ("1800-06-01", "1.1"),
    ("1800-06-02", "2.2"),
    ("1800-06-03", "3.3"),
    ("1800-06-04", "4.4"),
]
start, end = "1800-06-02", "1800-06-03"
route = "/history/{code}"

def expected(selected):
    values = [Decimal(r) for _, r in selected]
    mean = (sum(values) / len(values)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
    return {
        "count": len(selected),
        "min": min(selected, key=lambda p: Decimal(p[1]))[1],
        "max": max(selected, key=lambda p: Decimal(p[1]))[1],
        "mean": f"{mean:.6f}",
        "points": [{"date": d, "rate": r} for d, r in selected],
    }

cases = [
    ({"start": start, "end": end}, [p for p in points if start <= p[0] <= end]),
    ({"start": start}, [p for p in points if p[0] >= start]),
    ({"end": end}, [p for p in points if p[0] <= end]),
    ({}, points),
]
with db_session() as db:
    for date, rate in points:
        db.rates.replace_rate(date=date, currency=code, rate=rate)
    db.rates.replace_rate(date=start, currency="ZZC", rate="99")
    client = web_client()
    for params, selected in cases:
        resp = client.get(route.format(code=code), params=params)
        assert resp.status_code == 200, params
        body = resp.json()
        want = expected(selected)
        for key, value in want.items():
            assert body[key] == value, (params, key)
=== END AC history-bounds-inclusive ===

=== AC history-mean-half-even ===
Intent: The mean rounds half to even at six decimals: 0.000002 and 0.000003 average to a tie that half-even resolves to the even neighbour, not half-up.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZT"
points = [("1800-10-01", "0.000002"), ("1800-10-02", "0.000003")]
route = "/history/{code}"
with db_session() as db:
    for date, rate in points:
        db.rates.replace_rate(date=date, currency=code, rate=rate)
    client = web_client()
    resp = client.get(route.format(code=code))
    assert resp.status_code == 200
    body = resp.json()

values = [Decimal(r) for _, r in points]
exact = sum(values) / len(values)
mean = exact.quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
assert body["mean"] == f"{mean:.6f}"
=== END AC history-mean-half-even ===

=== AC history-currency-isolation ===
Intent: History for one currency never includes another currency's rates published on the same dates, and the response echoes the requested currency.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

mine, other = "ZZM", "ZZN"
dates = ["1800-11-01", "1800-11-02"]
route = "/history/{code}"
with db_session() as db:
    for i, date in enumerate(dates):
        db.rates.replace_rate(date=date, currency=mine, rate=f"{i + 1}.5")
        db.rates.replace_rate(date=date, currency=other, rate=f"{i + 7}.5")
    client = web_client()
    resp = client.get(route.format(code=mine))
    assert resp.status_code == 200
    body = resp.json()

assert body["currency"] == mine
assert [p["date"] for p in body["points"]] == dates
assert [p["rate"] for p in body["points"]] == [f"{i + 1}.5" for i in range(len(dates))]
=== END AC history-currency-isolation ===

## User Acceptance

- None.

## Guardrails

- Rates are read as stored text; statistics use `decimal`, never floating point.
- `min` and `max` are stored text exactly as published, never reformatted.
- Application code reaches the store only through `db.rates.history`.
