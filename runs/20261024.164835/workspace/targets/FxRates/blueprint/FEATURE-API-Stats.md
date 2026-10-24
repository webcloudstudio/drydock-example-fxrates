# FEATURE: API Statistics and Currencies

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Reports publication statistics and currencies with stored rates. |
| Depends On  | DATABASE.md, FEATURE-API-Foundation.md |
| Provides    | GET /stats, GET /currencies |
| Consumes    | rates repository operations |

## Purpose

Expose stored publication counts, date bounds, and the sorted set of currencies that have rates.

## Database Interface

- `FEATURE-API-005` — read: list stored rates for statistics and currencies - supplies: — - returns: `date`, `currency`, `rate`

## Routes

### `GET /stats`

Return the number of distinct publication dates, the number of stored rates, and the first and last publication dates. Both date fields are `null` when there are no rates.

### `GET /currencies`

Return base EUR and every currency with at least one stored rate, in ascending order.

## Programmatic Acceptance

=== AC stats-and-currencies-read-store ===
Intent: The statistics and currencies endpoints reflect rates stored through the persistence interface.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-01-02"
currencies = ("ZZZ", "AAA")
rates = ("0.943", "1.25")
with db_session() as db:
    before = db.rates.all()
    for currency, rate in zip(currencies, rates):
        db.rates.replace_rate(date=date, currency=currency, rate=rate)
    after = db.rates.all()

expected_dates = {row.date for row in before}
expected_dates.add(date)
expected_rate_count = len(before) + len(currencies)
expected_currencies = sorted({row.currency for row in after})

client = web_client()
stats = client.get("/stats")
assert stats.status_code == 200
body = stats.json()
assert body["dates"] == len(expected_dates)
assert body["rates"] == expected_rate_count
assert body["first"] == min(row.date for row in after)
assert body["last"] == max(row.date for row in after)

currencies_response = client.get("/currencies")
assert currencies_response.status_code == 200
currency_body = currencies_response.json()
assert currency_body["base"] == "EUR"
assert currency_body["currencies"] == expected_currencies
=== END AC stats-and-currencies-read-store ===

## User Acceptance

- None.

## Guardrails

- Derive counts, bounds, and currencies from stored rates.
- Return only currencies with at least one stored rate, sorted ascending.
