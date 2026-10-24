# FEATURE: Currency History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Returns bounded currency rate history with exact summary statistics. |
| Depends On  | FEATURE-API-Foundation.md, DATABASE.md |
| Provides    | GET /history/{code} |
| Consumes    | rates repository operations |

## Purpose

Return publication points for a currency, optionally bounded by inclusive `start` and `end` dates. Points are ordered by publication date ascending. The response includes `currency`, `base` (`EUR`), `count`, `min`, `max`, `mean`, and `points`.

`min` and `max` are the stored text of the smallest and largest rate by numeric value. `mean` is calculated exactly and rounded half-even to six decimal places, with exactly six decimals in its string representation. When the requested bounds contain no points, return count zero, null summary values, and an empty points array. A currency with no stored history at all returns 404.

## Programmatic Acceptance

=== AC history-route-returns-bounded-summary ===
Intent: The history route returns the supplied points and summary derived from their rates.

from decimal import Decimal, ROUND_HALF_EVEN
from persistence.testing import db_session
from app_server.testing import web_client

currency = "ZZU"
dates = ["2098-04-01", "2098-04-03"]
rates = ["1.25", "2.75"]
with db_session() as db:
    for date, rate in zip(dates, rates):
        db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get(
    f"/history/{currency}", params={"start": dates[0], "end": dates[-1]}
)
assert response.status_code == 200
body = response.json()
expected_mean = (sum((Decimal(value) for value in rates), Decimal(0)) / len(rates)).quantize(
    Decimal("0.000001"), rounding=ROUND_HALF_EVEN
)
assert body["currency"] == currency
assert body["base"] == "EUR"
assert body["count"] == len(dates)
assert body["min"] == min(rates, key=Decimal)
assert body["max"] == max(rates, key=Decimal)
assert body["mean"] == f"{expected_mean:.6f}"
assert [point["date"] for point in body["points"]] == dates
assert [point["rate"] for point in body["points"]] == rates
=== END AC history-route-returns-bounded-summary ===

=== AC history-route-empty-range ===
Intent: A currency with stored history returns the declared empty summary for a range with no points.

from persistence.testing import db_session
from app_server.testing import web_client

currency = "ZZT"
date = "2098-04-05"
rate = "1.25"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get(f"/history/{currency}", params={"start": "2098-04-06"})
assert response.status_code == 200
body = response.json()
assert body["count"] == 0
assert body["min"] is None
assert body["max"] is None
assert body["mean"] is None
assert body["points"] == []
=== END AC history-route-empty-range ===
