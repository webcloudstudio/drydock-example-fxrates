# FEATURE: Effective-Date Rates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Retrieves rates for the latest publication date on or before a requested date. |
| Depends On  | DATABASE.md, ARCHITECTURE.md |
| Provides    | GET /rates/{date}, GET /rates/latest |
| Consumes    | `FEATURE-RATE-002` rates.list_date, `FEATURE-RATE-005` rates.list_all |

## Purpose

Return the ECB rates for the effective publication date. A requested date resolves to the latest stored publication date on or before it.

## Workflow

- `GET /rates/{date}` accepts a real calendar date in `YYYY-MM-DD` form. A malformed date returns 422. If no publication exists on or before it, return 404.
- `GET /rates/latest` resolves the latest stored publication and uses `latest` as the requested value. Return 404 when there are no rates.
- Successful responses contain the effective date, requested date, EUR base, and every rate stored for that date. Rate values remain published text strings.

## Database Interface

- `FEATURE-RATE-002` — read: list rates for a publication date - supplies: `date` - returns: `date`, `currency`, `rate`
- `FEATURE-RATE-005` — read: list all rates - supplies: — - returns: `date`, `currency`, `rate`

## Guardrails

- Resolve effective dates from stored rows; do not hardcode dates or rates.
- Do not convert rate text to floating point.

## Programmatic Acceptance

=== AC rates-effective-date ===
Intent: A request between two arranged publications uses the earlier publication and returns its stored text.

from persistence.testing import db_session
from app_server.testing import web_client

requested = "2098-03-06"
effective = "2098-03-05"
currency = "ZZZ"
rate = "0.943"
with db_session() as db:
    db.rates.upsert(date=effective, currency=currency, rate=rate)
    db.rates.upsert(date="2098-03-07", currency=currency, rate="0.944")
    response = web_client().get(f"/rates/{requested}")
    assert response.status_code == 200
    body = response.json()
    assert body["date"] == effective
    assert body["requested"] == requested
    assert body["base"] == "EUR"
    assert body["rates"][currency] == rate
=== END AC rates-effective-date ===

=== AC rates-errors ===
Intent: The rates routes reject malformed dates and dates with no prior publication using their declared statuses.

from app_server.testing import web_client

client = web_client()
assert client.get("/rates/2025-13-01").status_code == 422
assert client.get("/rates/1900-01-01").status_code == 404
assert client.get("/rates/latest").status_code == 404
=== END AC rates-errors ===
