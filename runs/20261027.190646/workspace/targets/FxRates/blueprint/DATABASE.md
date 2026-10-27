# DATABASE: FxRates

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Persistence store and typed repository operations for the ECB euro reference rates held by FxRates. |
| Depends On | ARCHITECTURE.md |
| Provides | db.rates.replace_rate, db.rates.list_through, db.rates.list_all, db.rates.history |
| Build Order | 1 |

## Persistence Boundary

| Boundary | Rule |
|----------|------|
| Raw storage access | Only the generated `persistence/` package reaches the store. |
| Caller dependency | Features depend on declared access patterns and their DTOs, not on schemas. |
| Implementation | Generated from this file at the DATABASE build step; never written by hand. |
| Rate values | Stored as the ECB's published text and never converted to floating point. Arithmetic on them uses `decimal` in the caller. |
| Aggregation | Effective date, statistics, currency lists and history statistics are computed by callers from list operations. |

## Access Patterns

### FEATURE-RATE-001 — Store a rate, replacing the stored one

| Field | Value |
|-------|-------|
| Owner | DATABASE.md |
| Access | write |
| Repository operation | `rates.replace_rate` |
| Kind | upsert |
| Match | `date`, `currency` |
| Compatibility | unchanged |

Input: RatesReplaceRateInput

| Field | Type | Notes |
|-------|------|-------|
| date | str | `YYYY-MM-DD` |
| currency | str | Three-letter uppercase code |
| rate | str | Published text, stored exactly |

Output: RatesReplaceRateOutput

| Field | Type | Notes |
|-------|------|-------|
| date | str | Stored date |
| currency | str | Stored currency |
| rate | str | Stored rate text |

### FEATURE-RATE-002 — List rates on or before a date

| Field | Value |
|-------|-------|
| Owner | DATABASE.md |
| Access | read |
| Repository operation | `rates.list_through` |
| Kind | list |
| Match | `date <= through_date` |
| Order | `date` desc, `currency` asc |
| Compatibility | unchanged |

Input: RatesListThroughInput

| Field | Type | Notes |
|-------|------|-------|
| through_date | str | Optional upper bound, inclusive; omitted lists every rate |

Output: RatesListThroughOutput

| Field | Type | Notes |
|-------|------|-------|
| date | str | Publication date |
| currency | str | Currency code |
| rate | str | Rate text |

### FEATURE-RATE-003 — List every stored rate

| Field | Value |
|-------|-------|
| Owner | DATABASE.md |
| Access | read |
| Repository operation | `rates.list_all` |
| Kind | list |
| Order | `date` asc, `currency` asc |
| Compatibility | unchanged |

Input: RatesListAllInput

| Field | Type | Notes |
|-------|------|-------|

Output: RatesListAllOutput

| Field | Type | Notes |
|-------|------|-------|
| date | str | Publication date |
| currency | str | Currency code |
| rate | str | Rate text |

### FEATURE-RATE-004 — List a currency's history over a period

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

| Field | Type | Notes |
|-------|------|-------|
| currency | str | Currency code |
| start_date | str | Optional lower bound, inclusive |
| end_date | str | Optional upper bound, inclusive |

Output: RatesHistoryOutput

| Field | Type | Notes |
|-------|------|-------|
| date | str | Publication date |
| rate | str | Rate text |

## Schemas

## `rates`

| Field | Type | Notes |
|-------|------|-------|
| id | INTEGER PK | Surrogate key |
| date | TEXT NOT NULL | `YYYY-MM-DD` publication date |
| currency | TEXT NOT NULL | Three-letter uppercase currency code |
| rate | TEXT NOT NULL | Rate exactly as the ECB publishes it |

- UNIQUE (date, currency)

## Migrations

Each relational change has one staged record in `migrations/MIGRATION-<AccessPatternId>.md`.
The record carries Alembic `upgrade`/`downgrade` snippets and progresses from `planned` to `built`
only when its DATABASE build story completes. Alembic records deployment application separately.

| Access Pattern | Revision | State |
|----------------|----------|-------|

## Config (.env)

| Key | Type | Required | Notes |
|-----|------|----------|-------|
| DATABASE_URL | str | No | SQLite file path, optionally prefixed `sqlite://`; first choice |
| DATABASE_PATH | str | No | SQLite file path used when DATABASE_URL is unset; default `data/app.db` |

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

=== AC rates-replace-rate ===
Intent: Upserting the same date and currency twice leaves one row holding the second published text, and the first call returns the row it stored.
Requires: executable=python3; scope=test

from persistence.testing import db_session

date = "1800-01-01"
currency = "ZZA"
first = "1.2300"
second = "4.5"

with db_session() as db:
    stored = db.rates.replace_rate(date=date, currency=currency, rate=first)
    assert stored.date == date
    assert stored.currency == currency
    assert stored.rate == first
    db.rates.replace_rate(date=date, currency=currency, rate=second)
    rows = db.rates.history(currency=currency, start_date=date, end_date=date)
    assert len(rows) == 1
    assert rows[0].date == date
    assert rows[0].rate == second
=== END AC rates-replace-rate ===

=== AC rates-list-through ===
Intent: list_through returns only rates on or before the bound, ordered by date descending then currency ascending, and with no bound it also includes later dates.
Requires: executable=python3; scope=test

from persistence.testing import db_session

d1, d2, d3 = "1800-02-01", "1800-02-02", "1800-02-03"
items = [
    (d1, "ZZA", "1.1"),
    (d2, "ZZB", "2.2"),
    (d2, "ZZA", "3.3"),
    (d3, "ZZA", "4.4"),
]
mine = {d1, d2, d3}

with db_session() as db:
    for date, currency, rate in items:
        db.rates.replace_rate(date=date, currency=currency, rate=rate)

    by_currency = sorted(items, key=lambda t: t[1])
    ordered = sorted(by_currency, key=lambda t: t[0], reverse=True)

    bounded = db.rates.list_through(through_date=d2)
    got = [(r.date, r.currency, r.rate) for r in bounded if r.date in mine]
    assert got == [t for t in ordered if t[0] <= d2]

    unbounded = db.rates.list_through()
    got_all = [(r.date, r.currency, r.rate) for r in unbounded if r.date in mine]
    assert got_all == ordered
=== END AC rates-list-through ===

=== AC rates-list-all ===
Intent: list_all returns every stored rate ordered by date ascending then currency ascending, so a YYY code precedes ZZZ on one date.
Requires: executable=python3; scope=test

from persistence.testing import db_session

d1, d2 = "1800-03-01", "1800-03-02"
items = [
    (d2, "ZZZ", "9.9"),
    (d1, "ZZZ", "8.8"),
    (d2, "YYY", "7.7"),
    (d1, "YYY", "6.6"),
]
mine = {d1, d2}

with db_session() as db:
    before = len([r for r in db.rates.list_all() if r.date in mine])
    for date, currency, rate in items:
        db.rates.replace_rate(date=date, currency=currency, rate=rate)
    rows = db.rates.list_all()
    got = [(r.date, r.currency, r.rate) for r in rows if r.date in mine]
    assert len(got) == before + len(items)
    assert got == sorted(items, key=lambda t: (t[0], t[1]))
=== END AC rates-list-all ===

=== AC rates-history ===
Intent: history returns one currency's points ascending by date, honouring optional inclusive start and end bounds and excluding other currencies.
Requires: executable=python3; scope=test

from persistence.testing import db_session

currency = "ZZH"
other = "ZZI"
points = [
    ("1800-04-03", "3.3"),
    ("1800-04-01", "1.1"),
    ("1800-04-02", "2.2"),
    ("1800-04-04", "4.4"),
]
start, end = "1800-04-02", "1800-04-03"

with db_session() as db:
    for date, rate in points:
        db.rates.replace_rate(date=date, currency=currency, rate=rate)
    db.rates.replace_rate(date="1800-04-02", currency=other, rate="9.9")

    ordered = sorted(points, key=lambda t: t[0])

    rows = db.rates.history(currency=currency)
    assert [(r.date, r.rate) for r in rows] == ordered

    rows = db.rates.history(currency=currency, start_date=start)
    assert [(r.date, r.rate) for r in rows] == [p for p in ordered if p[0] >= start]

    rows = db.rates.history(currency=currency, end_date=end)
    assert [(r.date, r.rate) for r in rows] == [p for p in ordered if p[0] <= end]

    rows = db.rates.history(currency=currency, start_date=start, end_date=end)
    assert [(r.date, r.rate) for r in rows] == [p for p in ordered if start <= p[0] <= end]

    rows = db.rates.history(currency="ZZN")
    assert rows == []
=== END AC rates-history ===

## User Acceptance

- None.

## Guardrails

- Rates are stored as text exactly as published and are never stored or compared as floating point.
- Application code never opens a database driver, authors SQL or DDL, or reads the generated schema script.
- Ordinary application startup never initializes the schema; only `fxrates init` does, through `persistence.initialize_database(dsn)`.
- Initialization never drops tables, deletes rows, or migrates existing table definitions.
