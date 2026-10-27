# FEATURE: History Statistics

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | GET /history/{code} reports count, min, max, and mean over the points it returns. |
| Depends On | FEATURE-HistoryPoints.md |
| Provides | history statistics |
| Consumes | GET /history/{code} |

## Purpose

Add the summary fields `count`, `min`, `max`, and `mean` to the `/history/{code}` response, computed
over exactly the points the response lists.

## Behavior

- `count` is the number of points.
- `min` and `max` are the stored text, as JSON strings, of the smallest and largest rate by numeric
  value (compared as `Decimal`, never as text or float). The returned text is the stored text
  unchanged: `0.943` stays `0.943`.
- `mean` is the exact arithmetic mean of the point rates, computed with `decimal`, rounded half to
  even to six decimal places and written with exactly six decimals, as a JSON string.
- With no points, `count` is `0` and `min`, `max`, and `mean` are all `null`; `points` is `[]`.
- Statistics cover only the points inside the requested bounds.

## Database Interface

- None — persistence is owned by FEATURE-HistoryPoints.md.

## Programmatic Acceptance

=== AC history-stats-min-max-count ===
Intent: Count, min, and max are derived from the seeded rate texts by Decimal value, and min and max keep the stored text unchanged.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZH"
rates = {
    "1900-12-01": "0.9453",
    "1900-12-02": "0.943",
    "1900-12-03": "0.9441",
    "1900-12-04": "10.5",
    "1900-12-05": "9.75",
}

with db_session() as db:
    for d, r in rates.items():
        db.rates.replace_rate(date=d, currency=code, rate=r)
    client = web_client()
    resp = client.get(f"/history/{code}")
    assert resp.status_code == 200
    body = resp.json()
    texts = list(rates.values())
    assert body["count"] == len(texts)
    assert body["min"] == min(texts, key=Decimal)
    assert body["max"] == max(texts, key=Decimal)
=== END AC history-stats-min-max-count ===

=== AC history-stats-mean-half-even ===
Intent: Mean is the exact mean rounded half to even at six decimals and printed with six decimals; the two cases are exact ties at the seventh decimal, so they distinguish half-even from half-up.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN

from app_server.testing import web_client
from persistence.testing import db_session

cases = {
    "ZZM": {"1901-01-01": "1.000000", "1901-01-02": "1.000001"},
    "ZZN": {"1901-01-01": "1.000001", "1901-01-02": "1.000002"},
}

with db_session() as db:
    for code, rates in cases.items():
        for d, r in rates.items():
            db.rates.replace_rate(date=d, currency=code, rate=r)
    client = web_client()
    for code, rates in cases.items():
        resp = client.get(f"/history/{code}")
        assert resp.status_code == 200
        body = resp.json()
        total = sum(Decimal(r) for r in rates.values())
        mean = (total / len(rates)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
        assert body["mean"] == f"{mean:.6f}"
=== END AC history-stats-mean-half-even ===

=== AC history-stats-bounded ===
Intent: Statistics cover only the points inside the requested bounds, not the whole stored history.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZH"
rates = {
    "1901-02-01": "100",
    "1901-02-02": "1.5",
    "1901-02-03": "2.25",
    "1901-02-04": "0.5",
}
start = "1901-02-02"
end = "1901-02-03"

with db_session() as db:
    for d, r in rates.items():
        db.rates.replace_rate(date=d, currency=code, rate=r)
    client = web_client()
    resp = client.get(f"/history/{code}", params={"start": start, "end": end})
    assert resp.status_code == 200
    body = resp.json()
    inside = [rates[d] for d in sorted(rates) if start <= d <= end]
    assert body["count"] == len(inside)
    assert body["min"] == min(inside, key=Decimal)
    assert body["max"] == max(inside, key=Decimal)
    mean = (sum(Decimal(r) for r in inside) / len(inside)).quantize(
        Decimal("0.000001"), rounding=ROUND_HALF_EVEN
    )
    assert body["mean"] == f"{mean:.6f}"
=== END AC history-stats-bounded ===

=== AC history-stats-empty ===
Intent: A history with no points in range reports count 0 and null statistics with an empty points list, still as a 200.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZH"
stored = "1901-03-01"
after = "1901-04-01"

with db_session() as db:
    db.rates.replace_rate(date=stored, currency=code, rate="4")
    client = web_client()
    resp = client.get(f"/history/{code}", params={"start": after})
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == 0
    assert body["min"] is None
    assert body["max"] is None
    assert body["mean"] is None
    assert body["points"] == []
=== END AC history-stats-empty ===

## User Acceptance

- None.

## Guardrails

- Statistics use `decimal` exclusively; no floating-point arithmetic or comparison.
- `min` and `max` return stored text, never a re-formatted value.
- Rounding is half to even.
