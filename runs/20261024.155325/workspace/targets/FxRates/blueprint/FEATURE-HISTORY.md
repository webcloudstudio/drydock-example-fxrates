# FEATURE: Currency History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Returns a currency’s rate history and summary statistics. |
| Depends On  | DATABASE.md, FEATURE-API-FOUNDATION.md |
| Provides    | GET /history/{code} |
| Consumes    | rates.history |

## Purpose

Provide ascending rate points for a currency over optional inclusive date bounds, plus count, minimum, maximum, and mean.

## Workflow

`GET /history/{code}` accepts optional `start` and `end` dates. It reads rates through `db.rates.history`, returning points in ascending date order. The mean is computed using `Decimal` and rounded half-even to six decimal places, with exactly six digits after the decimal point. Minimum and maximum are selected by numeric value and returned as their stored text.

If the currency has no stored rate at all, including EUR, return 404. If it has stored rates but none within the requested range, return 200 with count `0`, null statistics, and an empty points list. Malformed date bounds return 422.

## Programmatic Acceptance

=== AC history-points-and-statistics ===
Intent: The history endpoint returns the selected stored points and summary values.

from app_server.testing import web_client
from persistence.testing import db_session

currency = "TST"
start = "2099-01-02"
end = "2099-01-04"
rates = ["1.0", "2.0", "3.0"]
with db_session() as db:
    for date, rate in zip([start, "2099-01-03", end], rates):
        db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get(f"/history/{currency}", params={"start": start, "end": end})
body = response.json()
assert response.status_code == 200
assert body["currency"] == currency
assert body["count"] == len(rates)
assert [point["rate"] for point in body["points"]] == rates
assert [point["date"] for point in body["points"]] == [start, "2099-01-03", end]
=== END AC history-points-and-statistics ===

=== AC history-empty-range ===
Intent: A stored currency with no points in the requested range returns empty statistics.

from app_server.testing import web_client
from persistence.testing import db_session

currency = "TST"
stored_date = "2099-01-02"
start = "2099-01-03"
end = "2099-01-04"
with db_session() as db:
    db.rates.upsert(date=stored_date, currency=currency, rate="1")

response = web_client().get(f"/history/{currency}", params={"start": start, "end": end})
assert response.status_code == 200
assert response.json()["count"] == 0
assert response.json()["points"] == []
=== END AC history-empty-range ===

=== AC history-unknown-currency ===
Intent: A currency with no stored rates returns 404 from its history endpoint.

from app_server.testing import web_client

response = web_client().get("/history/UNUSED")
assert response.status_code == 404
=== END AC history-unknown-currency ===

=== AC history-invalid-bound ===
Intent: A malformed date bound is rejected with 422.

from app_server.testing import web_client

response = web_client().get("/history/TST", params={"start": "2099-02-30"})
assert response.status_code == 422
=== END AC history-invalid-bound ===

## User Acceptance

- None.

## Guardrails

- Read rates only through the declared persistence interface.
- Perform arithmetic with `Decimal`, never floating point.

## Database Interface

- `FEATURE-DATA-004` — read: rates.history - supplies: `currency`, `start_date`, `end_date` - returns: `date`, `currency`, `rate`
