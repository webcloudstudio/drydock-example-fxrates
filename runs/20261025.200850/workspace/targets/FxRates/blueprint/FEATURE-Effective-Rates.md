# FEATURE: Effective Rates

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Retrieves published rates for a requested date or the latest available publication. |
| Depends On  | FEATURE-API-Foundation.md, DATABASE.md |
| Provides    | GET /rates/{date}, GET /rates/latest |
| Consumes    | rates repository operations |

## Purpose

Return the rates for the latest publication date on or before a requested calendar date, or the latest publication for the dedicated latest route.

## Routes

- `GET /rates/{date}` accepts a real `YYYY-MM-DD` date. It returns the effective publication date, echoes the requested date, base `EUR`, and all rates on that publication date.
- `GET /rates/latest` returns the latest publication with `"requested": "latest"`.
- A date before the first publication returns 404. A malformed date returns 422.

## Database Interface

- `FEATURE-RATE-003` — read: list stored rates - supplies: `currency`, `start_date`, `end_date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC effective-date-rates ===
Intent: Both rate routes resolve an effective date and preserve the supplied published rate text.

from app_server.testing import web_client
from persistence.testing import db_session

earlier_day = "2099-01-02"
later_day = "2099-01-05"
requested_day = "2099-01-06"
currency = "XTS"
earlier_rate = "1.2300"
later_rate = "1.240"
with db_session() as db:
    db.rates.upsert(date=earlier_day, currency=currency, rate=earlier_rate)
    db.rates.upsert(date=later_day, currency=currency, rate=later_rate)

client = web_client()
response = client.get("/rates/" + requested_day)
latest = client.get("/rates/latest")
assert response.status_code == 200
assert response.json() == {
    "date": later_day,
    "requested": requested_day,
    "base": "EUR",
    "rates": {currency: later_rate},
}
assert latest.status_code == 200
assert latest.json()["date"] == later_day
assert latest.json()["requested"] == "latest"
assert latest.json()["rates"][currency] == later_rate
=== END AC effective-date-rates ===

=== AC effective-date-errors ===
Intent: Requests before available history return 404 and malformed calendar dates return 422.

from app_server.testing import web_client
from persistence.testing import db_session

day = "2099-01-02"
with db_session() as db:
    db.rates.upsert(date=day, currency="XTS", rate="1.2")

client = web_client()
assert client.get("/rates/2098-01-01").status_code == 404
assert client.get("/rates/2099-13-01").status_code == 422
=== END AC effective-date-errors ===

## User Acceptance

- None.

## Guardrails

- Effective-date selection is inclusive: use the latest publication on or before the request.
- Return all currencies available on the effective publication date.
- Preserve published rate text in JSON strings; do not convert rates to floating point.
