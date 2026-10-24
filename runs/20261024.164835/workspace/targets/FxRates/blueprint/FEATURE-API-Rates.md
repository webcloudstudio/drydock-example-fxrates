# FEATURE: API Rates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Returns rates for an effective publication date or the latest publication. |
| Depends On  | DATABASE.md, FEATURE-API-Foundation.md, FEATURE-ECB-Load.md |
| Provides    | GET /rates/{date}, GET /rates/latest |
| Consumes    | rates repository operations |

## Purpose

Serve stored rates using the latest publication on or before the requested date. The latest route identifies its request as `latest`.

## Database Interface

- `FEATURE-API-001` — read: list rates for an effective date - supplies: `date` - returns: `date`, `currency`, `rate`
- `FEATURE-API-002` — read: find the latest publication on or before a date - supplies: `requested_date` - returns: `date`, `currency`, `rate`
- `FEATURE-API-003` — read: find the latest publication - supplies: — - returns: `date`, `currency`, `rate`

## Routes

### `GET /rates/{date}`

Return the effective publication date, requested date, EUR base, and all rates stored for that publication. Return 404 if no publication exists on or before the requested date.

### `GET /rates/latest`

Return the same shape using the latest publication, with `requested` set to `latest`. Return 404 when the store has no publication.

## Programmatic Acceptance

=== AC effective-and-latest-rates ===
Intent: Both rates routes return persisted values for the effective and latest publication.

from app_server.testing import web_client
from persistence.testing import db_session

dates = ("2099-01-02", "2099-01-03")
currency = "ZZZ"
rates = ("0.943", "1.25")
with db_session() as db:
    for date, rate in zip(dates, rates):
        db.rates.replace_rate(date=date, currency=currency, rate=rate)

client = web_client()
effective = client.get(f"/rates/{dates[1]}")
assert effective.status_code == 200
effective_body = effective.json()
assert effective_body["date"] == dates[1]
assert effective_body["requested"] == dates[1]
assert effective_body["base"] == "EUR"
assert effective_body["rates"] == {currency: rates[1]}

latest = client.get("/rates/latest")
assert latest.status_code == 200
latest_body = latest.json()
assert latest_body["date"] == dates[1]
assert latest_body["requested"] == "latest"
assert latest_body["rates"] == {currency: rates[1]}

earliest_request = client.get("/rates/2098-12-31")
assert earliest_request.status_code == 404
=== END AC effective-and-latest-rates ===

## User Acceptance

- None.

## Guardrails

- Resolve dates to the latest stored publication on or before the requested date.
- Rates are returned as their stored text; EUR is the base currency.
