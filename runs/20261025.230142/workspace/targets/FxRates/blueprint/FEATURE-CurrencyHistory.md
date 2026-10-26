# FEATURE: Currency History

| Field | Value |
|-------|-------|
| Version | 20261025 V1 |
| Description | Retrieve ordered currency history and statistics over optional date bounds. |
| Depends On | FEATURE-ApiFoundation.md, DATABASE.md |
| Provides | GET /history/{code} |
| Consumes | rates repository operations |

## Purpose

Return a currency’s stored publication points in ascending date order, optionally filtered by inclusive `start` and `end` bounds. Include count, minimum and maximum by numeric rate value, and the exact arithmetic mean rounded half to even to six decimal places and formatted with six decimals. Preserve rate text for points and extrema. When there are no points, return count zero and null statistics with an empty points list. A currency with no stored rate at all returns 404.

## Database Interface


- None — persistence is owned by FEATURE-InitializeRates.md, FEATURE-LoadHistory.md.

## Programmatic Acceptance

=== AC history_points_and_mean ===
Intent: History returns stored points in date order and computes count and mean from their exact decimal values.
Requires: python-package=httpx; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from persistence.testing import db_session
from app_server.testing import web_client

currency = "ZZZ"
dates = ["2099-01-03", "2099-01-01", "2099-01-02"]
rates = ["3.00", "1.00", "2.00"]
with db_session() as db:
    for date, rate in zip(dates, rates):
        db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get(f"/history/{currency}")
assert response.status_code == 200
body = response.json()
expected_dates = sorted(dates)
expected_mean = (sum(map(Decimal, rates)) / Decimal(len(rates))).quantize(
    Decimal("0.000001"), rounding=ROUND_HALF_EVEN
)
assert [point["date"] for point in body["points"]] == expected_dates
assert [point["rate"] for point in body["points"]] == [
    rates[dates.index(date)] for date in expected_dates
]
assert body["currency"] == currency
assert body["count"] == len(rates)
assert body["mean"] == f"{expected_mean:.6f}"
=== END AC history_points_and_mean ===

=== AC history_bounds_and_empty_range ===
Intent: Inclusive date bounds select matching history points and an empty range has null statistics.
Requires: python-package=httpx; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

currency = "ZZZ"
dates = ["2099-01-01", "2099-01-02"]
rates = ["1.00", "2.00"]
with db_session() as db:
    for date, rate in zip(dates, rates):
        db.rates.upsert(date=date, currency=currency, rate=rate)

client = web_client()
bounded = client.get(
    f"/history/{currency}",
    params={"start": dates[0], "end": dates[0]},
)
empty = client.get(f"/history/{currency}", params={"start": "2099-02-01"})
assert bounded.status_code == 200
assert empty.status_code == 200
assert [point["date"] for point in bounded.json()["points"]] == [dates[0]]
assert bounded.json()["count"] == 1
assert empty.json()["count"] == 0
assert empty.json()["min"] is None
assert empty.json()["max"] is None
assert empty.json()["mean"] is None
assert empty.json()["points"] == []
=== END AC history_bounds_and_empty_range ===

## User Acceptance

- None.

## Guardrails

- Date bounds are optional and inclusive.
- Order points by ascending publication date.
- Use exact Decimal statistics and preserve published rate text.
- A currency with no stored rate at all returns 404.
