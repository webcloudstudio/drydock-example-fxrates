# FEATURE: API History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Serves a currency's stored rate history and summary statistics. |
| Depends On  | DATABASE.md, FEATURE-API-Foundation.md |
| Provides    | GET /history/{code} |
| Consumes    | rates.history |

## Purpose

Return a currency's publication points and statistics for an optional date range.

## Workflow

1. Receive a currency code and optional `start` and `end` dates.
2. Return 404 if the currency has no stored rate at all, including EUR.
3. Query the inclusive date range in ascending date order.
4. Return the points, count, minimum and maximum published rate text, and the exact mean rounded half to even to six decimal places.
5. If the range has no points, return count zero, null statistics, and an empty points list.

## Database Interface

- `FEATURE-API-004` — read: list a currency's rates in an inclusive date range - supplies: `currency`, `start_date`, `end_date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC history-points-and-statistics ===
Intent: The history route returns inclusive, ascending points and statistics derived from the seeded rates.

from decimal import Decimal, ROUND_HALF_EVEN
from persistence.testing import db_session
from app_server.testing import web_client

currency = "ZZZ"
seed = [("2099-01-02", "1.1"), ("2099-01-03", "1.2")]
with db_session() as db:
    for date, rate in seed:
        db.rates.replace_rate(date=date, currency=currency, rate=rate)

response = web_client().get(f"/history/{currency}", params={"start": seed[0][0], "end": seed[1][0]})
assert response.status_code == 200
body = response.json()
assert [point["date"] for point in body["points"]] == [date for date, _ in seed]
assert [point["rate"] for point in body["points"]] == [rate for _, rate in seed]
assert body["count"] == len(seed)
values = [Decimal(rate) for _, rate in seed]
assert body["min"] == str(min(values))
assert body["max"] == str(max(values))
mean = (sum(values) / len(values)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
assert body["mean"] == f"{mean:.6f}"
=== END AC history-points-and-statistics ===

=== AC history-empty-range ===
Intent: A known currency with no points inside the selected bounds returns empty-range statistics.

from persistence.testing import db_session
from app_server.testing import web_client

currency = "ZZZ"
date = "2099-01-02"
with db_session() as db:
    db.rates.replace_rate(date=date, currency=currency, rate="1.1")

response = web_client().get(f"/history/{currency}", params={"start": "2100-01-01"})
assert response.status_code == 200
body = response.json()
assert body["currency"] == currency
assert body["count"] == 0
assert body["min"] is None and body["max"] is None and body["mean"] is None
assert body["points"] == []
=== END AC history-empty-range ===

=== AC history-unknown-currency ===
Intent: A currency with no stored history returns 404.

from app_server.testing import web_client

response = web_client().get("/history/ZZZ")
assert response.status_code == 404
=== END AC history-unknown-currency ===

## User Acceptance

- None.

## Guardrails

- Date bounds are optional and inclusive.
- Points are returned in ascending date order.
- Rate text is preserved; statistics use exact Decimal arithmetic.
- The mean uses half-even rounding to six decimal places.
- A currency with no stored rates returns 404; a known currency with no points in the selected range returns empty statistics.
