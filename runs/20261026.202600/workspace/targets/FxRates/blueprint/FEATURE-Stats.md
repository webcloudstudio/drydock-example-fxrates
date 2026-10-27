# FEATURE: Stored Rate Statistics

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Defines the API summary of stored publication dates and rates. |
| Depends On  | FEATURE-AppServer.md, DATABASE.md |
| Provides    | GET /stats |
| Consumes    | create_app(), rates repository operations |

## Purpose

`GET /stats` reports the number of publication dates and stored rates, plus the earliest and latest publication dates. Empty date bounds are null. Values come from repository queries.

## Database Interface

- `FEATURE-RATE-005` — read: list stored rates - supplies: — - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC stats-derive-from-store ===
Intent: The statistics endpoint reflects rates inserted through the repository.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

first_date = "2099-07-01"
second_date = "2099-07-02"
currency = "QAG"

with db_session() as db:
    before_rows = db.rates.list()
    before_dates = {row.date for row in before_rows}
    db.rates.upsert(date=first_date, currency=currency, rate="7.1")
    db.rates.upsert(date=second_date, currency=currency, rate="7.2")
    after_rows = db.rates.list()
    expected_dates = before_dates | {first_date, second_date}
    expected_rate_count = len(before_rows) + 2

client = web_client()
response = client.get("/stats")
assert response.status_code == 200
body = response.json()
assert body["dates"] == len(expected_dates)
assert body["rates"] == expected_rate_count
assert body["first"] == min(expected_dates)
assert body["last"] == max(expected_dates)
=== END AC stats-derive-from-store ===

=== AC stats-empty-store ===
Intent: The statistics endpoint reports null date bounds when the rates store is empty.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    rows = db.rates.list()
    if rows:
        from cli.testing import cli_runner
        code, stdout, stderr = cli_runner("init")
        assert code == 0

client = web_client()
response = client.get("/stats")
assert response.status_code == 200
body = response.json()
assert body["dates"] == 0
assert body["rates"] == 0
assert body["first"] is None
assert body["last"] is None
=== END AC stats-empty-store ===

## User Acceptance

- None.

## Guardrails

- Derive all reported values from the rates repository.
- Do not store or compute rates as floating-point values.
