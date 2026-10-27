# FEATURE: Rate Storage

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Store parsed rate records through the persistence library, replacing any rate already stored for the same date and currency. |
| Depends On | DATABASE.md, ARCHITECTURE.md |
| Provides | ratestore.store_rates |
| Consumes | db.rates.replace_rate |

## Purpose

`ratestore.store_rates(db, records)` writes validated rate records into the `rates` table. It is the only write path for loaded rates and uses the declared upsert so reloading is idempotent.

## Interface

- Module `ratestore`, function `store_rates(db, records) -> tuple[int, int]`.
- `db` is an open persistence `Database`; `records` is any iterable of three-item sequences `(date, currency, rate)` such as `ecb.Rate` tuples.
- Each record is written with `db.rates.replace_rate(date=..., currency=..., rate=...)`.
- The return value is `(dates, rates)`: the number of distinct dates and the number of rates written from `records`.
- Empty `records` writes nothing and returns `(0, 0)`.
- The function neither opens nor closes the database and authors no SQL.

## Rules

1. A rate stored for a (`date`, `currency`) that already exists replaces the stored text.
2. Writing the same records again leaves the stored rows unchanged and returns the same counts.
3. Rate text is stored exactly as given.

## Database Interface

- `FEATURE-RATE-001` — write: store a rate, replacing the stored one - supplies: `date`, `currency`, `rate` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC ratestore-round-trip ===
Intent: Stored records read back through the history operation with their exact published text, and the returned counts equal the distinct dates and the records written.
Requires: executable=python3; scope=test

from persistence.testing import db_session
from ratestore import store_rates

d1, d2 = "1800-05-01", "1800-05-02"
records = [
    (d1, "ZZA", "1.2300"),
    (d1, "ZZB", "10"),
    (d2, "ZZA", "1.5"),
]

with db_session() as db:
    counts = store_rates(db, records)
    assert tuple(counts) == (len({r[0] for r in records}), len(records))
    for currency in ("ZZA", "ZZB"):
        rows = db.rates.history(currency=currency, start_date=d1, end_date=d2)
        got = [(r.date, r.rate) for r in rows]
        want = sorted((r[0], r[2]) for r in records if r[1] == currency)
        assert got == want
=== END AC ratestore-round-trip ===

=== AC ratestore-replace-and-idempotent ===
Intent: Storing the same records twice leaves one row per date and currency, and storing a changed rate replaces the stored text.
Requires: executable=python3; scope=test

from persistence.testing import db_session
from ratestore import store_rates

d = "1800-05-10"
first = [(d, "ZZA", "1.1"), (d, "ZZB", "2.2")]
changed = [(d, "ZZA", "9.90")]

with db_session() as db:
    store_rates(db, first)
    again = store_rates(db, first)
    assert tuple(again) == (1, len(first))
    rows = db.rates.history(currency="ZZA", start_date=d, end_date=d)
    assert [(r.date, r.rate) for r in rows] == [(d, first[0][2])]

    store_rates(db, changed)
    rows = db.rates.history(currency="ZZA", start_date=d, end_date=d)
    assert [(r.date, r.rate) for r in rows] == [(d, changed[0][2])]
    other = db.rates.history(currency="ZZB", start_date=d, end_date=d)
    assert [(r.date, r.rate) for r in other] == [(d, first[1][2])]
=== END AC ratestore-replace-and-idempotent ===

=== AC ratestore-empty ===
Intent: Empty input writes nothing and reports zero dates and zero rates.
Requires: executable=python3; scope=test

from persistence.testing import db_session
from ratestore import store_rates

with db_session() as db:
    before = len(db.rates.list_all())
    counts = store_rates(db, [])
    assert tuple(counts) == (0, 0)
    assert len(db.rates.list_all()) == before
=== END AC ratestore-empty ===

## User Acceptance

- None.

## Guardrails

- Rates are written only through `db.rates.replace_rate`; no SQL and no driver import appears in this module.
- Rate values are never converted to floating point.
