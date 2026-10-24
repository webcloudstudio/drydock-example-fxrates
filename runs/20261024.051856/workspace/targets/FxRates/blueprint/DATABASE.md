# DATABASE: FxRates

| Field | Value |
|-------|-------|
| Version | 20261024 V1 |
| Description | Persistence schema and typed repository operations for ECB reference rates. |
| Depends On | ARCHITECTURE.md |
| Provides | rates repository operations |

## Persistence Boundary

| Boundary | Rule |
|----------|------|
| Raw storage access | Only the generated `persistence/` package reaches SQLite. |
| Caller dependency | Features call declared `rates` repository operations and do not depend on schema details. |
| Rate representation | Store each ECB rate as the exact published text; never store a rate as a floating-point value. |
| Initialization | `fxrates init` resets the rates store through the supported persistence boundary. |

## Access Patterns

### FEATURE-RATE-001 — Read rates by publication date and currency

| Field | Value |
|-------|-------|
| Owner | DATABASE.md |
| Access | read |
| Repository operation | `rates.get` |
| Compatibility | unchanged |
| Match | `date`, `currency` |

Input: RateKey

| Field | Type |
|-------|------|
| date | str |
| currency | str |

Output: Rate

| Field | Type |
|-------|------|
| id | int |
| date | str |
| currency | str |
| rate | str |

### FEATURE-RATE-002 — List rates with optional equality filters

| Field | Value |
|-------|-------|
| Owner | DATABASE.md |
| Access | read |
| Repository operation | `rates.list` |
| Compatibility | unchanged |

Input: RateFilters

| Field | Type |
|-------|------|
| date | str |
| currency | str |

Output: Rate

| Field | Type |
|-------|------|
| id | int |
| date | str |
| currency | str |
| rate | str |

### FEATURE-RATE-003 — Store or replace a rate

| Field | Value |
|-------|-------|
| Owner | FEATURE-Load-History.md |
| Access | write |
| Repository operation | `rates.upsert` |
| Compatibility | unchanged |
| Match | `date`, `currency` |

Input: RateValues

| Field | Type |
|-------|------|
| date | str |
| currency | str |
| rate | str |

Output: Rate

| Field | Type |
|-------|------|
| id | int |
| date | str |
| currency | str |
| rate | str |

### FEATURE-RATE-004 — Delete one stored rate

| Field | Value |
|-------|-------|
| Owner | DATABASE.md |
| Access | write |
| Repository operation | `rates.delete` |
| Compatibility | unchanged |
| Match | `date`, `currency` |

Input: RateKey

| Field | Type |
|-------|------|
| date | str |
| currency | str |

Output: RateKey

| Field | Type |
|-------|------|
| date | str |
| currency | str |

## Schemas

## `rates`

| Field | Type | Notes |
|-------|------|-------|
| id | INTEGER PK | Surrogate row key. |
| date | TEXT NOT NULL | ECB publication date in `YYYY-MM-DD` form. |
| currency | TEXT NOT NULL | Three-letter uppercase currency code. |
| rate | TEXT NOT NULL | Exact published rate text. |

- UNIQUE (date, currency)

## Migrations

No migrations are required for this initial schema.

| Access Pattern | Revision | State |
|----------------|----------|-------|

## Config (.env)

| Key | Type | Required | Notes |
|-----|------|----------|-------|
| DATABASE_URL | str | No | SQLite database file path; takes precedence over `DATABASE_PATH`. |
| DATABASE_PATH | str | No | SQLite database file path used when `DATABASE_URL` is unset. |

When neither setting is provided, the application uses `data/app.db`.

## File Stores

| Store | Root dir | Notes |
|-------|----------|-------|

## External Services

| Service | Wrapper | Notes |
|---------|---------|-------|

## External Libraries

| Library | Ownership | Distribution | Consumer Contract |
|---------|-----------|--------------|-------------------|

## Programmatic Acceptance

=== AC rates-get ===
Intent: A rate can be retrieved by its unique publication date and currency key.

from persistence.testing import db_session

with db_session() as db:
    created = db.rates.upsert(date="2099-01-02", currency="ZZZ", rate="1.234")
    assert created is not None
    row = db.rates.get(date="2099-01-02", currency="ZZZ")
    assert row is not None
    assert row.date == created.date
    assert row.currency == created.currency
    assert row.rate == created.rate
=== END AC rates-get ===

=== AC rates-list ===
Intent: Rate rows can be listed and filtered by declared equality fields.

from persistence.testing import db_session

with db_session() as db:
    created = db.rates.upsert(date="2099-01-03", currency="ZZY", rate="2.345")
    assert created is not None
    rows = db.rates.list(date="2099-01-03")
    assert any(row.date == created.date and row.currency == created.currency and row.rate == created.rate for row in rows)
=== END AC rates-list ===

=== AC rates-upsert ===
Intent: Storing a rate inserts it and replaces the value for the same date and currency.

from persistence.testing import db_session

with db_session() as db:
    first = db.rates.upsert(date="2099-01-04", currency="ZZX", rate="3.456")
    assert first is not None
    replaced = db.rates.upsert(date="2099-01-04", currency="ZZX", rate="4.567")
    assert replaced is not None
    row = db.rates.get(date="2099-01-04", currency="ZZX")
    assert row is not None
    assert row.rate == replaced.rate
    assert row.date == first.date
=== END AC rates-upsert ===

=== AC rates-delete ===
Intent: A stored rate can be deleted by its unique publication date and currency key.

from persistence.testing import db_session

with db_session() as db:
    created = db.rates.upsert(date="2099-01-05", currency="ZZW", rate="5.678")
    assert created is not None
    deleted = db.rates.delete(date="2099-01-05", currency="ZZW")
    assert deleted is not None
    row = db.rates.get(date=created.date, currency=created.currency)
    assert row is None
=== END AC rates-delete ===

## User Acceptance

- None.

## Guardrails

- Every application database operation uses the generated persistence package.
- Rates remain text exactly as published; arithmetic is performed by application services with `decimal`.
