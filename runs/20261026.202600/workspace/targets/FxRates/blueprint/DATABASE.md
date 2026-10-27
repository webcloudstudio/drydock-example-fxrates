# DATABASE: FxRates

| Field | Value |
|-------|-------|
| Version | 20261026 V1 |
| Description | Declares the rates store and typed repository operations used by FxRates. |
| Depends On | ARCHITECTURE.md |
| Provides | rates repository operations |

## Persistence Boundary

| Boundary | Rule |
|----------|------|
| Raw storage access | Only the generated `persistence/` package reaches the store. |
| Caller dependency | Features use the declared repository operations and DTOs, not the schema. |
| Implementation | Drydock generates the persistence package and DDL from this declaration. |

## Access Patterns

### FEATURE-RATE-001 — Store or replace a published rate

| Field | Value |
|-------|-------|
| Owner | DATABASE.md |
| Access | write |
| Repository operation | `rates.upsert` |
| Compatibility | unchanged |
| Match | `date`, `currency` |

Input: RateUpsertInput

| Field | Type |
|-------|------|
| date | str |
| currency | str |
| rate | str |

Output: RateUpsertOutput

| Field | Type |
|-------|------|
| date | str |
| currency | str |
| rate | str |

### FEATURE-RATE-002 — List rates for a publication date

| Field | Value |
|-------|-------|
| Owner | DATABASE.md |
| Access | read |
| Repository operation | `rates.by_date` |
| Kind | list |
| Match | `date` |
| Order | `currency` asc |
| Compatibility | unchanged |

Input: RatesByDateInput

| Field | Type |
|-------|------|
| date | str |

Output: RatesByDateOutput

| Field | Type |
|-------|------|
| date | str |
| currency | str |
| rate | str |

### FEATURE-RATE-003 — Find publications on or before a date

| Field | Value |
|-------|-------|
| Owner | DATABASE.md |
| Access | read |
| Repository operation | `rates.publications_through` |
| Kind | list |
| Match | `date <= requested_date` |
| Order | `date` desc |
| Compatibility | unchanged |

Input: RatesPublicationsThroughInput

| Field | Type |
|-------|------|
| requested_date | str |

Output: RatesPublicationsThroughOutput

| Field | Type |
|-------|------|
| date | str |
| currency | str |
| rate | str |

### FEATURE-RATE-004 — List a currency's rates within optional date bounds

| Field | Value |
|-------|-------|
| Owner | DATABASE.md |
| Access | read |
| Repository operation | `rates.history` |
| Kind | list |
| Match | `currency`, `date >= start_date`, `date <= end_date` |
| Order | `date` asc |
| Compatibility | unchanged |

Input: RatesHistoryInput

| Field | Type |
|-------|------|
| currency | str |
| start_date | str |
| end_date | str |

Output: RatesHistoryOutput

| Field | Type |
|-------|------|
| date | str |
| currency | str |
| rate | str |

### FEATURE-RATE-005 — List stored rates

| Field | Value |
|-------|-------|
| Owner | DATABASE.md |
| Access | read |
| Repository operation | `rates.list` |
| Kind | list |
| Compatibility | unchanged |

Input: RatesListInput

| Field | Type |
|-------|------|

Output: RatesListOutput

| Field | Type |
|-------|------|
| date | str |
| currency | str |
| rate | str |

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

## Config (.env)

| Key | Type | Required | Notes |
|-----|------|----------|-------|
| DATABASE_URL | str | No | Database DSN; takes precedence over `DATABASE_PATH`. |
| DATABASE_PATH | str | No | Database file path used when `DATABASE_URL` is unset. |

## File Stores

| Store | Root dir | Notes |
|-------|----------|-------|

## External Services

| Service | Wrapper | Notes |
|---------|---------|-------|

## External Libraries

| Library | Ownership | Distribution | Consumer Contract |
|---------|-----------|--------------|-------------------|
| ECB reference rates | Fetch feature | ECB history ZIP | Fetch downloads and extracts the archive before passing its CSV through the load workflow. |

## Programmatic Acceptance

=== AC rates-upsert ===
Intent: The repository stores a rate and replaces the value for the same date and currency.

from persistence.testing import db_session

date = "2099-01-02"
currency = "QAA"
rate = "1.234"
replacement = "1.235"

with db_session() as db:
    first = db.rates.upsert(date=date, currency=currency, rate=rate)
    assert first.date == date
    assert first.currency == currency
    assert first.rate == rate

    second = db.rates.upsert(date=date, currency=currency, rate=replacement)
    assert second.rate == replacement

    stored = db.rates.by_date(date=date)
    assert len([row for row in stored if row.currency == currency]) == 1
    assert next(row for row in stored if row.currency == currency).rate == replacement
=== END AC rates-upsert ===

=== AC rates-by-date ===
Intent: The repository returns the stored rates for a requested publication date.

from persistence.testing import db_session

date = "2099-02-03"
currency = "QAB"
rate = "2.50"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)
    rows = db.rates.by_date(date=date)
    assert any(row.date == date and row.currency == currency and row.rate == rate for row in rows)
=== END AC rates-by-date ===

=== AC rates-publications-through ===
Intent: The repository returns stored publications on or before the requested date in descending date order.

from persistence.testing import db_session

earlier = "2099-03-01"
later = "2099-03-02"
requested = later
currency = "QAC"

with db_session() as db:
    db.rates.upsert(date=earlier, currency=currency, rate="3")
    db.rates.upsert(date=later, currency=currency, rate="4")
    rows = db.rates.publications_through(requested_date=requested)
    dates = list(dict.fromkeys(row.date for row in rows))
    assert dates == sorted(dates, reverse=True)
    assert earlier in dates
    assert later in dates
=== END AC rates-publications-through ===

=== AC rates-history ===
Intent: The repository returns a currency's rates within inclusive optional date bounds in ascending date order.

from persistence.testing import db_session

currency = "QAD"
start = "2099-04-02"
end = "2099-04-03"
before = "2099-04-01"
after = "2099-04-04"

with db_session() as db:
    db.rates.upsert(date=before, currency=currency, rate="1")
    db.rates.upsert(date=start, currency=currency, rate="2")
    db.rates.upsert(date=end, currency=currency, rate="3")
    db.rates.upsert(date=after, currency=currency, rate="4")
    rows = db.rates.history(currency=currency, start_date=start, end_date=end)
    assert [row.date for row in rows] == [start, end]
=== END AC rates-history ===

=== AC rates-list ===
Intent: The repository lists stored rates with their published text.

from persistence.testing import db_session

date = "2099-05-06"
currency = "QAE"
rate = "5.006"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)
    rows = db.rates.list()
    assert any(row.date == date and row.currency == currency and row.rate == rate for row in rows)
=== END AC rates-list ===

## User Acceptance

- None.

## Guardrails

- Preserve every ECB rate as published text; do not store or compute rates as floating-point values.
- Application code accesses the database only through the shipped persistence library and generated relational layer.
- Database location resolves from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- Keep the `(date, currency)` uniqueness rule so loading an existing rate replaces that stored value.
