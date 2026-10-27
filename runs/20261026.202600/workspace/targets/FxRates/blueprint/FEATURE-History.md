# FEATURE: Currency History

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Returns a currency's stored rate history and summary statistics over optional bounds. |
| Depends On  | FEATURE-AppServer.md, DATABASE.md |
| Provides    | GET /history/{code} |
| Consumes    | create_app(), rates repository operations |

## Purpose

Return a currency's publication points and min, max, and mean statistics over an optional inclusive date range.

## Trigger and workflow

A caller requests a currency history with optional `start` and `end` dates. Malformed bounds return `422`. Return points in ascending date order and preserve each published rate string. Return `404` if the currency has no stored history at all, including EUR. If it has history but no points in the selected range, return count zero, null min/max/mean, and an empty points list.

Compute minimum and maximum by numeric value. Compute the exact mean using `Decimal` and round half-even to six decimal places.

## Database Interface

- `FEATURE-RATE-004` — read: list a currency's rates within optional inclusive bounds - supplies: `currency`, `start_date`, `end_date` - returns: `date`, `currency`, `rate`
- `FEATURE-RATE-005` — read: determine whether the currency has any stored rate - supplies: none - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC history-range-and-statistics ===
Intent: The history endpoint returns bounded points and statistics derived from the seeded rates.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from app_server.testing import web_client
from persistence.testing import db_session

currency = "QAK"
dates = ["2099-09-01", "2099-09-02", "2099-09-03"]
rates = ["1.1", "1.3", "1.2"]
start = dates[0]
end = dates[2]

with db_session() as db:
    for date, rate in zip(dates, rates):
        db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get(f"/history/{currency}", params={"start": start, "end": end})
body = response.json()
expected_mean = (sum((Decimal(rate) for rate in rates), Decimal(0)) / len(rates)).quantize(
    Decimal("0.000001"), rounding=ROUND_HALF_EVEN
)
assert response.status_code == 200
assert body["currency"] == currency
assert body["base"] == "EUR"
assert [point["date"] for point in body["points"]] == dates
assert [point["rate"] for point in body["points"]] == rates
assert body["count"] == len(rates)
assert body["min"] == min(rates, key=Decimal)
assert body["max"] == max(rates, key=Decimal)
assert body["mean"] == f"{expected_mean:.6f}"
=== END AC history-range-and-statistics ===

=== AC history-empty-range-and-errors ===
Intent: The history endpoint distinguishes an empty range from a currency with no history and rejects malformed bounds.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

currency = "QAL"
date = "2099-10-01"
rate = "1.4"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

client = web_client()
empty = client.get(f"/history/{currency}", params={"start": "2099-10-02"})
assert empty.status_code == 200
assert empty.json()["count"] == 0
assert empty.json()["min"] is None
assert empty.json()["max"] is None
assert empty.json()["mean"] is None
assert empty.json()["points"] == []
assert client.get("/history/QAM").status_code == 404
assert client.get(f"/history/{currency}", params={"start": "2099-10-01-x"}).status_code == 422
=== END AC history-empty-range-and-errors ===

## User Acceptance

- None.

## Guardrails

- Preserve stored rate text for history points and min/max values.
- Use exact decimal arithmetic for mean and round half-even to six decimal places.
- Treat a currency with no history as 404, distinct from an empty bounded result.
