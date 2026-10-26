# FEATURE: Effective Rates

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Resolves stored rates for a requested or latest ECB publication date. |
| Depends On  | ARCHITECTURE.md, DATABASE.md, FEATURE-HistoryLoading.md |
| Provides    | GET /rates/{date}, GET /rates/latest |
| Consumes    | rates.effective_rates, rates.by_date |

## Purpose

Return the rates for the latest publication date on or before a valid requested date. The latest endpoint resolves the most recent stored publication date.

## Behavior

- `GET /rates/{date}` accepts a real calendar date in `YYYY-MM-DD` form and returns `{"date": effective_date, "requested": requested_date, "base": "EUR", "rates": {currency: published_rate_text}}`.
- `GET /rates/latest` returns the same shape, with `"requested": "latest"`.
- Rates include every currency stored on the effective date, in a JSON object.
- Return 404 when no publication exists on or before the requested date, or when the database contains no rates.
- A malformed path date returns 422.
- Choose the effective date using `rates.effective_rates`; fetch that date's full set with `rates.by_date`.

## Database Interface

- `FEATURE-RATE-002` — read: find rates on or before a date - supplies: `as_of` - returns: `date`, `currency`, `rate`
- `FEATURE-RATE-003` — read: list rates for one date - supplies: `date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC effective-rate-routes ===
Intent: Both effective-rate routes return successful responses for dates backed by rates.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx; scope=test

from app_server.testing import web_client
from cli.testing import cli_runner
from persistence.testing import db_session

with db_session() as db:
    for date, currency, rate in [
        ("2099-01-01", "AAA", "1.25"),
        ("2099-01-01", "ZZZ", "2.5"),
    ]:
        db.rates.upsert(date=date, currency=currency, rate=rate)

client = web_client()
assert client.get("/rates/2099-01-01").status_code == 200
assert client.get("/rates/latest").status_code == 200
=== END AC effective-rate-routes ===

=== AC effective-rate-errors ===
Intent: A malformed requested date is rejected, and a date before all stored rates is not found.

Requires: python-package=fastapi; scope=test
Requires: python-package=httpx; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    db.rates.upsert(date="2099-02-02", currency="AAA", rate="1.25")

client = web_client()
assert client.get("/rates/not-a-date").status_code == 422
assert client.get("/rates/2099-02-01").status_code == 404
=== END AC effective-rate-errors ===

## User Acceptance

- None.

## Guardrails

- Preserve published rate text in responses.
- Never compute rates with floating point.
