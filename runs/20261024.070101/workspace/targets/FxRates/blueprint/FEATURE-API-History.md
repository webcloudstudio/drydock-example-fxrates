# FEATURE: Currency History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Returns a currency's stored rate history and summary statistics. |
| Depends On  | DATABASE.md |
| Provides    | GET /history/{code} |
| Consumes    | rates repository operations |

## Purpose

Return ascending publication-date points for a currency, optionally bounded by inclusive `start` and `end` dates. Rates, minimum, and maximum preserve stored text. Compute the exact mean with decimal arithmetic and half-even rounding to six decimal places. When the selected range has no points, return an empty points list, count zero, and null statistics. Return 404 when the currency has no stored rate at all.

## Database Interface

- `FEATURE-RATE-002` — read: list rates with optional date and currency filters - supplies: `date`, `currency` - returns: `id`, `date`, `currency`, `rate`

## Programmatic Acceptance

Requires: python-package=httpx; scope=test

=== AC history-range ===
Intent: The history endpoint returns the stored rate as a point for an inclusive single-date range.

from persistence.testing import db_session
from app_server.testing import web_client

publication = "2099-01-02"
currency = "ZZZ"
rate = "1.2300"
with db_session() as db:
    db.rates.upsert(date=publication, currency=currency, rate=rate)

response = web_client().get(
    f"/history/{currency}", params={"start": publication, "end": publication}
)
body = response.json()
assert response.status_code == 200
assert body["currency"] == currency
assert body["count"] == 1
assert body["points"] == [{"date": publication, "rate": rate}]
assert body["min"] == rate
assert body["max"] == rate
assert body["mean"] == "1.230000"
=== END AC history-range ===

=== AC history-empty-range ===
Intent: A known currency with no points in the selected range returns empty statistics.

from persistence.testing import db_session
from app_server.testing import web_client

publication = "2099-01-02"
currency = "ZZZ"
with db_session() as db:
    db.rates.upsert(date=publication, currency=currency, rate="1.23")

response = web_client().get(
    f"/history/{currency}", params={"start": "1999-01-01", "end": "1999-01-02"}
)
body = response.json()
assert response.status_code == 200
assert body["count"] == 0
assert body["min"] is None
assert body["max"] is None
assert body["mean"] is None
assert body["points"] == []
=== END AC history-empty-range ===

=== AC history-malformed-bound ===
Intent: A malformed date bound is rejected with the request-validation status.

from app_server.testing import web_client

response = web_client().get("/history/ZZZ", params={"start": "2099-13-01"})
assert response.status_code == 422
=== END AC history-malformed-bound ===

=== AC history-unknown-currency ===
Intent: A currency with no stored history returns not found.

from app_server.testing import web_client

response = web_client().get("/history/ZZZ")
assert response.status_code == 404
=== END AC history-unknown-currency ===

## User Acceptance

- None.

## Guardrails

- Preserve stored rate text in points, minimum, and maximum.
- Calculate the mean with exact decimal arithmetic and half-even rounding.
