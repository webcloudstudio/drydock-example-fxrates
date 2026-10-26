# FEATURE: Currency History

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Returns a currency’s stored rates and summary statistics over a date range. |
| Depends On  | ARCHITECTURE.md, DATABASE.md, FEATURE-HistoryLoading.md |
| Provides    | GET /history/{code} |
| Consumes    | rates.history |

## Purpose

Return the stored history for one currency across an inclusive optional date range, with summary statistics.

## Behavior

- `start` and `end` are optional valid calendar dates. Include points on either bound and return points in ascending date order.
- Each point includes the stored rate as published text.
- Report `count`, `min`, `max`, and `mean`. `min` and `max` are the stored text for the lowest and highest rates by numeric value.
- Compute mean exactly with decimal arithmetic, round half to even to six decimal places, and format with exactly six decimals.
- If there are no points, return count zero, null statistics, and an empty points array.
- Return 404 when the currency has no stored rate at all, including EUR. A valid currency and range with no points returns the empty-period response.
- Malformed date bounds return 422.

## Database Interface

- `FEATURE-RATE-004` — read: retrieve a currency's history in date bounds - supplies: `currency`, `start_date`, `end_date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC history-route ===
Intent: The history route returns stored points in ascending date order for the requested currency and range.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

currency = "ZZZ"
first_date = "2099-04-01"
second_date = "2099-04-02"
rate = "1.5"

with db_session() as db:
    db.rates.upsert(date=second_date, currency=currency, rate=rate)
    db.rates.upsert(date=first_date, currency=currency, rate=rate)

response = web_client().get(
    f"/history/{currency}",
    params={"start": first_date, "end": second_date},
)
assert response.status_code == 200
body = response.json()
assert [point["date"] for point in body["points"]] == [first_date, second_date]
assert [point["rate"] for point in body["points"]] == [rate, rate]
=== END AC history-route ===

=== AC history-summary-and-empty ===
Intent: History reports the count and extrema of stored points and represents a valid empty period with null statistics.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from app_server.testing import web_client
from persistence.testing import db_session

currency = "ZZZ"
date = "2099-04-03"
rate = "1.5"
expected_mean = Decimal(rate).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

client = web_client()
response = client.get(f"/history/{currency}")
assert response.status_code == 200
body = response.json()
assert body["count"] == 1
assert body["min"] == rate
assert body["max"] == rate
assert body["mean"] == f"{expected_mean:.6f}"

empty = client.get(f"/history/{currency}", params={"start": "2099-04-04"})
assert empty.status_code == 200
empty_body = empty.json()
assert empty_body["count"] == 0
assert empty_body["min"] is None
assert empty_body["max"] is None
assert empty_body["mean"] is None
assert empty_body["points"] == []
=== END AC history-summary-and-empty ===

=== AC history-errors ===
Intent: History rejects malformed date bounds and an unavailable currency.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    db.rates.upsert(date="2099-04-05", currency="AAA", rate="2")

client = web_client()
assert client.get("/history/AAA", params={"start": "2025-13-01"}).status_code == 422
assert client.get("/history/NOX").status_code == 404
=== END AC history-errors ===

## User Acceptance

- None.

## Guardrails

- Keep rates as published text in point and extrema responses.
- Use Decimal for numeric comparisons and the mean.
