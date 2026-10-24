# DATABASE: FxRates

| Field | Value |
|-------|-------|
| Version | 20261024 V1 |
| Description | Persistence schema and typed repository operations for ECB exchange rates. |
| Depends On | ARCHITECTURE.md |
| Provides | rates.list, rates.upsert, rates.delete |
| Consumes | persistence.open_database |

## Persistence Boundary

| Boundary | Rule |
|----------|------|
| Raw storage access | Only the generated `persistence/` package reaches SQLite. |
| Caller dependency | Features call declared repository operations and use their DTOs; they do not depend on the schema. |
| Implementation | Generated from this file at the DATABASE build step and never written by hand. |

## Access Patterns

### FEATURE-RATE-001 — List rates

| Field | Value |
|-------|-------|
| Owner | FEATURE-Rate-Loading.md |
| Access | read |
| Repository operation | `rates.list` |
| Compatibility | unchanged |

Input: `RatesListInput`

| Field | Type | Required |
|-------|------|----------|
| date | str | no |
| currency | str | no |

Output: `RateRow`

| Field | Type |
|-------|------|
| id | int |
| date | str |
| currency | str |
| rate | str |

### FEATURE-RATE-002 — Replace a rate

| Field | Value |
|-------|-------|
| Owner | FEATURE-Rate-Loading.md |
| Access | write |
| Repository operation | `rates.upsert` |
| Match | `date`, `currency` |
| Compatibility | unchanged |

Input: `RateUpsertInput`

| Field | Type | Required |
|-------|------|----------|
| date | str | yes |
| currency | str | yes |
| rate | str | yes |

Output: `RateRow`

| Field | Type |
|-------|------|
| id | int |
| date | str |
| currency | str |
| rate | str |

### FEATURE-RATE-003 — Delete a rate

| Field | Value |
|-------|-------|
| Owner | FEATURE-CLI.md |
| Access | write |
| Repository operation | `rates.delete` |
| Match | `date`, `currency` |
| Compatibility | unchanged |

Input: `RateDeleteInput`

| Field | Type | Required |
|-------|------|----------|
| date | str | yes |
| currency | str | yes |

Output: `RateDeleteResult`

| Field | Type |
|-------|------|
| date | str |
| currency | str |

## Schemas

## `rates`

| Field | Type | Notes |
|-------|------|-------|
| id | INTEGER PK | Generated row identifier. |
| date | TEXT NOT NULL | ECB publication date in `YYYY-MM-DD` form. |
| currency | TEXT NOT NULL | Three-letter uppercase currency code. |
| rate | TEXT NOT NULL | ECB-published rate text, preserved exactly. |

- UNIQUE (date, currency)

## Migrations

| Access Pattern | Revision | State |
|----------------|----------|-------|
| FEATURE-RATE-001 | — | planned |
| FEATURE-RATE-002 | — | planned |
| FEATURE-RATE-003 | — | planned |

## Config (.env)

| Key | Type | Required | Notes |
|-----|------|----------|-------|
| DATABASE_URL | str | no | SQLite file path or `sqlite://` DSN; takes precedence. |
| DATABASE_PATH | str | no | SQLite file path used when `DATABASE_URL` is unset. |

When both keys are unset, the application uses `data/app.db`.

## File Stores

| Store | Root dir | Notes |
|-------|----------|-------|
| — | — | No file store is used for persistent application state. |

## External Services

| Service | Wrapper | Notes |
|---------|---------|-------|
| — | — | No external service is accessed by the persistence layer. |

## External Libraries

| Library | Ownership | Distribution | Consumer Contract |
|---------|-----------|--------------|-------------------|
| Shipped persistence package | Generated persistence boundary | Supplied by Drydock | Application code calls `open_database` and declared `db.rates` operations; it does not open a database driver. |

## Programmatic Acceptance

=== AC rates-list ===
Intent: Listing returns the rows created through the declared repository interface.

from persistence.testing import db_session

with db_session() as db:
    date = "2099-01-02"
    currency = "QAZ"
    rate = "1.234"
    db.rates.upsert(date=date, currency=currency, rate=rate)
    rows = db.rates.list(date=date, currency=currency)
    assert len(rows) == 1
    assert rows[0].date == date
    assert rows[0].currency == currency
    assert rows[0].rate == rate
=== END AC rates-list ===

=== AC rates-upsert ===
Intent: Upserting the same date and currency replaces the stored rate.

from persistence.testing import db_session

with db_session() as db:
    date = "2099-01-03"
    currency = "QAZ"
    first_rate = "1.234"
    replacement_rate = "1.235"
    db.rates.upsert(date=date, currency=currency, rate=first_rate)
    db.rates.upsert(date=date, currency=currency, rate=replacement_rate)
    rows = db.rates.list(date=date, currency=currency)
    assert len(rows) == 1
    assert rows[0].date == date
    assert rows[0].currency == currency
    assert rows[0].rate == replacement_rate
=== END AC rates-upsert ===

=== AC rates-delete ===
Intent: Deleting a matching date and currency removes that rate.

from persistence.testing import db_session

with db_session() as db:
    date = "2099-01-04"
    currency = "QAZ"
    rate = "1.234"
    db.rates.upsert(date=date, currency=currency, rate=rate)
    removed = db.rates.delete(date=date, currency=currency)
    assert removed.date == date
    assert removed.currency == currency
    assert db.rates.list(date=date, currency=currency) == []
=== END AC rates-delete ===

## User Acceptance

- None.

## Guardrails

- Preserve published rates as text; do not convert them to floating point during storage.
- Keep the `(date, currency)` natural key unique so replacement is atomic and unambiguous.
- All runtime database access goes through the generated persistence package.
