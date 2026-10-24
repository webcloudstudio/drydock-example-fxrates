# FEATURE: CLI Load

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Loads validated ECB history files into the rates store and reports the imported totals. |
| Depends On  | DATABASE.md |
| Provides    | fxrates load |
| Consumes    | rates repository operations |

## Purpose

Load an ECB euro reference history CSV into the rates store. A rejected file must leave stored data unchanged.

## Workflow

1. Read the requested CSV file.
2. Validate the complete file before writing any rates.
3. For each row, store every valid rate as its exact published text; skip `N/A`.
4. Replace an existing rate with the same date and currency.
5. Report `dates,rates`, followed by the number of dates with at least one stored rate and the number of rates stored from this file.

The header begins with `Date`; subsequent fields are three-letter uppercase currency codes. Ignore the trailing empty field produced by the ECB's trailing comma. Dates must be real, unique `YYYY-MM-DD` dates within the file. Each row must have the expected field count. Rate values must match `[0-9]+(\.[0-9]+)?` and be nonzero, or be `N/A`.

A malformed row, repeated or invalid date, or invalid rate rejects the whole file before the first write, returning exit code 3. An unreadable file returns exit code 1. Failures produce no standard output and one diagnostic line on standard error.

## Database Interface

- `FEATURE-RATE-001` — write: store or replace a rate - supplies: `date`, `currency`, `rate` - returns: `id`, `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC load-valid-file ===
Intent: A valid staged ECB file loads successfully and its rows can be read back through the rates repository.

from cli.testing import cli_runner
from persistence.testing import db_session

code, out, err = cli_runner("load", "sources/eurofxref-hist_2025-02-03_04.csv")
assert code == 0

with db_session() as db:
    rows = db.rates.list(date="2025-02-04")
    by_currency = {row.currency: row.rate for row in rows}
    assert len(rows) == 8
    assert by_currency["USD"] == "1.0335"
    assert by_currency["CNY"] == "7.4943"
=== END AC load-valid-file ===

=== AC load-rejects-whole-file ===
Intent: A file containing an invalid rate is rejected without storing any of its rows.

from cli.testing import cli_runner
from persistence.testing import db_session

code, out, err = cli_runner("load", "sources/eurofxref-hist_bad.csv")
assert code == 3

with db_session() as db:
    assert db.rates.list(date="2025-02-03") == []
=== END AC load-rejects-whole-file ===

## User Acceptance

- None.

## Guardrails

- Validate every row before the first write.
- Preserve published rate text and never store `N/A`.
- Replace existing values for the same date and currency.
- Do not read the harness or data files from application code.
- Access rates only through the generated persistence package.
