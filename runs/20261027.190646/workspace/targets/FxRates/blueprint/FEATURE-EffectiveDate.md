# FEATURE: Effective Date

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Service function that resolves the latest publication date on or before a requested date and returns that date's rates. |
| Depends On | DATABASE.md, ARCHITECTURE.md |
| Provides | rates.effective_publication |
| Consumes | db.rates.list_through |

## Purpose

The ECB publishes on working days only. A request for date `D` uses the latest publication date on or
before `D`. This service is the single place that rule lives; the rates and conversion routes call it.

## Interface

Module `services/effective_date.py` (a top-level `services` package):

`effective_publication(db, requested: str | None) -> tuple[str, dict[str, str]] | None`

- `requested` is an ISO `YYYY-MM-DD` string, or `None` meaning the latest publication.
- Makes exactly one `db.rates.list_through(...)` call: with `through_date=requested` when a date is given,
  with no bound when `None`.
- The rows arrive ordered by date descending then currency ascending. The first row's date is the
  effective date. The rates are the rows carrying that date, as a mapping of currency code to stored rate text.
- Returns `None` when no row exists on or before the requested date.
- Dates are compared as ISO strings. Rate values are the stored text, never converted to a number.

## Database Interface

- `FEATURE-RATE-002` — read: list rates on or before a date - supplies: `through_date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC effective-date-exact-and-between ===
Intent: A requested date that is a publication uses itself, and a later requested date uses the latest earlier publication; only the effective date's rates are returned as stored text.
Requires: executable=python3; scope=test

from persistence.testing import db_session
from services.effective_date import effective_publication

older = "1800-05-08"
newer = "1800-05-10"
later_request = "1800-05-12"
older_rates = {"ZZA": "1.1000", "ZZB": "9.9"}
newer_rates = {"ZZA": "2.2500", "ZZB": "8.8", "ZZC": "7"}

with db_session() as db:
    for cur, rate in older_rates.items():
        db.rates.replace_rate(date=older, currency=cur, rate=rate)
    for cur, rate in newer_rates.items():
        db.rates.replace_rate(date=newer, currency=cur, rate=rate)

    found = effective_publication(db, newer)
    assert found is not None
    date, rates = found
    assert date == newer
    assert rates == newer_rates

    found = effective_publication(db, later_request)
    assert found is not None
    date, rates = found
    assert date == newer
    assert rates == newer_rates

    found = effective_publication(db, "1800-05-09")
    assert found is not None
    date, rates = found
    assert date == older
    assert rates == older_rates
=== END AC effective-date-exact-and-between ===

=== AC effective-date-none-before ===
Intent: A requested date earlier than every stored publication yields None rather than an error or an empty result.
Requires: executable=python3; scope=test

from persistence.testing import db_session
from services.effective_date import effective_publication

seeded = "1800-05-20"
too_early = "1799-01-01"

with db_session() as db:
    db.rates.replace_rate(date=seeded, currency="ZZA", rate="1.5")
    assert effective_publication(db, too_early) is None
=== END AC effective-date-none-before ===

=== AC effective-date-latest ===
Intent: Passing None resolves the latest publication in the store; a far-future seeded date is always the latest regardless of existing data.
Requires: executable=python3; scope=test

from persistence.testing import db_session
from services.effective_date import effective_publication

latest = "9999-12-31"
rates_in = {"ZZA": "3.1400", "ZZB": "2.7"}

with db_session() as db:
    for cur, rate in rates_in.items():
        db.rates.replace_rate(date=latest, currency=cur, rate=rate)
    found = effective_publication(db, None)
    assert found is not None
    date, rates = found
    assert date == latest
    assert rates == rates_in
    for value in rates.values():
        assert isinstance(value, str)
=== END AC effective-date-latest ===

## User Acceptance

- None.

## Guardrails

- Rate values stay as stored text; no float or Decimal conversion happens in this service.
- The function reaches the store only through `db.rates.list_through`.
- Dates are compared as ISO strings, never via floating point or locale parsing.
