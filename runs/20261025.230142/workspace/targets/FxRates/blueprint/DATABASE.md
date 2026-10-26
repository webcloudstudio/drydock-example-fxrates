# DATABASE: FxRates

| Field | Value |
|-------|-------|
| Version | 20261025 V1 |
| Description | Persistence stores and typed repository interfaces for ECB currency rates. |
| Depends On | ARCHITECTURE.md |
| Provides | rates repository operations |
| Consumes | |

## Persistence Boundary

| Boundary | Rule |
|----------|------|
| Raw storage access | Only the generated `persistence/` package reaches the store. |
| Caller dependency | Features depend on declared access patterns and their DTOs, not on schemas. |
| Implementation | Generated from this file at the DATABASE build step; never written by hand. |

## Access Patterns

### FEATURE-RATE-001 — Retrieve a rate by date and currency

| Field | Value |
|-------|-------|
| Owner | FEATURE-LoadHistory.md |
| Access | read |
| Repository operation | `rates.get` |
| Compatibility | unchanged |
| Match | `date`, `currency` |

Input: RatesGetInput

| Field | Type |
|-------|------|
| date | str |
| currency | str |

Output: RatesGetOutput

| Field | Type |
|-------|------|
| date | str |
| currency | str |
| rate | str |

### FEATURE-RATE-002 — List rates with optional date and currency filters

| Field | Value |
|-------|-------|
| Owner | FEATURE-LoadHistory.md |
| Access | read |
| Repository operation | `rates.list` |
| Compatibility | unchanged |
| Match | `currency`, `date >= start_date`, `date <= end_date` |
| Order | `date` asc, `currency` asc |

Input: RatesListInput

| Field | Type |
|-------|------|
| currency | str |
| start_date | str |
| end_date | str |

Output: RatesListOutput

| Field | Type |
|-------|------|
| date | str |
| currency | str |
| rate | str |

### FEATURE-RATE-003 — Replace or store a published rate

| Field | Value |
|-------|-------|
| Owner | FEATURE-LoadHistory.md |
| Access | write |
| Repository operation | `rates.upsert` |
| Compatibility | unchanged |
| Match | `date`, `currency` |

Input: RatesUpsertInput

| Field | Type |
|-------|------|
| date | str |
| currency | str |
| rate | str |

Output: RatesUpsertOutput

| Field | Type |
|-------|------|
| date | str |
| currency | str |
| rate | str |

### FEATURE-RATE-004 — Delete a stored rate

| Field | Value |
|-------|-------|
| Owner | FEATURE-InitializeRates.md |
| Access | write |
| Repository operation | `rates.delete` |
| Compatibility | unchanged |
| Match | `date`, `currency` |

Input: RatesDeleteInput

| Field | Type |
|-------|------|
| date | str |
| currency | str |

Output: RatesDeleteOutput

| Field | Type |
|-------|------|
| date | str |
| currency | str |

## Schemas

## `rates`

| Field | Type | Notes |
|-------|------|-------|
| id | INTEGER PK | Internal row identifier. |
| date | TEXT NOT NULL | ECB publication date in `YYYY-MM-DD` form. |
| currency | TEXT NOT NULL | Three-letter uppercase currency code. |
| rate | TEXT NOT NULL | ECB-published rate text, unchanged. |

- UNIQUE (date, currency)

## Migrations

Each relational change has one staged record in `migrations/MIGRATION-<AccessPatternId>.md`.
The record carries Alembic `upgrade`/`downgrade` snippets and progresses from `planned` to `built`
only when its DATABASE build story completes. Alembic records deployment application separately.

| Access Pattern | Revision | State |
|----------------|----------|-------|
| FEATURE-RATE-001 | — | planned |
| FEATURE-RATE-002 | — | planned |
| FEATURE-RATE-003 | — | planned |
| FEATURE-RATE-004 | — | planned |

## Config (.env)

| Key | Type | Required | Notes |
|-----|------|----------|-------|
| `DATABASE_URL` | str | No | Database DSN; takes precedence over `DATABASE_PATH`. |
| `DATABASE_PATH` | str | No | Database file path when `DATABASE_URL` is unset. |
| Default | str | No | `data/app.db` when neither environment variable is set. |

## File Stores

| Store | Root dir | Notes |
|-------|----------|-------|
| — | — | No file store. |

## External Services

| Service | Wrapper | Notes |
|---------|---------|-------|
| — | — | No runtime external service. |

## External Libraries

| Library | Ownership | Distribution | Consumer Contract |
|---------|-----------|--------------|-------------------|
| ECB archive download | FEATURE-FetchHistory.md | Python standard library | Fetch story owns download and ZIP extraction; automated tests replace the download with a stub. |

## Programmatic Acceptance

=== AC rates_get_round_trip ===
Intent: Retrieve a stored rate by its date and currency through the declared repository operation.

from persistence.testing import db_session

date = "2099-01-02"
currency = "ZZZ"
rate = "1.2300"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)
    row = db.rates.get(date=date, currency=currency)

assert row.date == date
assert row.currency == currency
assert row.rate == rate
=== END AC rates_get_round_trip ===

=== AC rates_list_filters_and_order ===
Intent: List stored rates in date and currency order and filter by currency and inclusive date bounds.

from persistence.testing import db_session

currency = "ZZZ"
other_currency = "YYY"
dates = ["2099-01-03", "2099-01-01", "2099-01-02"]
rates = ["3.00", "1.00", "2.00"]

with db_session() as db:
    for date, rate in zip(dates, rates):
        db.rates.upsert(date=date, currency=currency, rate=rate)
    db.rates.upsert(date=dates[1], currency=other_currency, rate="8.00")

    all_rows = db.rates.list()
    filtered = db.rates.list(
        currency=currency,
        start_date=dates[1],
        end_date=dates[2],
    )

assert [(row.date, row.currency, row.rate) for row in all_rows if row.date in dates] == [
    ("2099-01-01", currency, "1.00"),
    ("2099-01-01", other_currency, "8.00"),
    ("2099-01-02", currency, "2.00"),
    ("2099-01-03", currency, "3.00"),
]
assert [(row.date, row.currency, row.rate) for row in filtered] == [
    (dates[1], currency, rates[1]),
    (dates[2], currency, rates[2]),
]
=== END AC rates_list_filters_and_order ===

=== AC rates_upsert_replaces ===
Intent: Upsert replaces an existing date and currency rate while preserving its published text.

from persistence.testing import db_session

date = "2099-02-01"
currency = "ZZZ"
original = "1.20"
replacement = "1.2000"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=original)
    db.rates.upsert(date=date, currency=currency, rate=replacement)
    row = db.rates.get(date=date, currency=currency)

assert row.rate == replacement
=== END AC rates_upsert_replaces ===

=== AC rates_delete_round_trip ===
Intent: Delete removes the selected date and currency rate from the repository.

from persistence.testing import db_session

date = "2099-03-01"
currency = "ZZZ"
rate = "4.50"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)
    deleted = db.rates.delete(date=date, currency=currency)
    row = db.rates.get(date=date, currency=currency)

assert deleted.date == date
assert deleted.currency == currency
assert row is None
=== END AC rates_delete_round_trip ===

## User Acceptance

- None.

## Guardrails

- Store each ECB rate exactly as published, using text and never floating point.
- Reject an invalid input file before the first write; a rejected file changes nothing.
- Replace an existing rate with the same date and currency.
- Resolve the store from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- Application code accesses SQLite only through the generated persistence package.
- Do not modify or read `sources/run.sh` or supplied data files from application code.
