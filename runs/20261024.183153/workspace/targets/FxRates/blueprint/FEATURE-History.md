# FEATURE: Currency History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Returns ordered currency rate history and exact summary statistics for an inclusive date range. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /history/{code} |
| Consumes    | rates persistence operations |

## Purpose

Let callers retrieve a currency’s published rates and summary statistics over an optional inclusive date range.

## Trigger and workflow

A caller requests `GET /history/{code}` with optional `start` and `end` dates. The service reads the currency’s stored rates, filters the requested bounds inclusively, and returns points in ascending date order. It computes minimum and maximum by numeric value and the mean using exact decimal arithmetic, rounded half-even to six decimal places.

If the currency has no stored rate, including EUR, return 404. If the currency exists but the requested range has no points, return an empty result with null statistics. Malformed date bounds return 422.

## Database Interface

- `FEATURE-RATE-004` — read: determine whether a currency has stored rates - supplies: `currency` - returns: `date`, `rate`
- `FEATURE-RATE-005` — read: retrieve currency rates in an inclusive date range - supplies: `currency`, `start_date`, `end_date` - returns: `date`, `rate`

## Programmatic Acceptance

=== AC history-present ===
Intent: A stored currency has an accessible history point with its published rate text.

from persistence.testing import db_session
from app_server.testing import web_client

date = "2098-12-30"
currency = "QZX"
rate_text = "8.765"
with db_session() as db:
    db.rates.replace_rate(date=date, currency=currency, rate=rate_text)

response = web_client().get(f"/history/{currency}")
assert response.status_code == 200
body = response.json()
assert body["currency"] == currency
assert any(point["date"] == date and point["rate"] == rate_text for point in body["points"])
=== END AC history-present ===

=== AC history-empty-range ===
Intent: An existing currency with no rates in the selected range returns empty statistics.

from persistence.testing import db_session
from app_server.testing import web_client

currency = "QZY"
date = "2098-12-30"
with db_session() as db:
    db.rates.replace_rate(date=date, currency=currency, rate="7.654")

response = web_client().get(f"/history/{currency}", params={"start": "2098-12-31"})
assert response.status_code == 200
body = response.json()
assert body["count"] == 0
assert body["min"] is None
assert body["max"] is None
assert body["mean"] is None
assert body["points"] == []
=== END AC history-empty-range ===

=== AC history-errors ===
Intent: Unknown currencies return 404 and malformed date bounds return 422.

from persistence.testing import db_session
from app_server.testing import web_client

date = "2098-12-30"
currency = "QZW"
with db_session() as db:
    db.rates.replace_rate(date=date, currency=currency, rate="6.543")

client = web_client()
assert client.get("/history/UNKNOWN").status_code == 404
assert client.get(f"/history/{currency}", params={"end": "not-a-date"}).status_code == 422
=== END AC history-errors ===

## User Acceptance

- None.

## Guardrails

- Preserve published rate text in returned points and min/max values.
- Use Decimal arithmetic; do not use floating-point calculations.
- Do not access the database outside the shipped persistence library.
