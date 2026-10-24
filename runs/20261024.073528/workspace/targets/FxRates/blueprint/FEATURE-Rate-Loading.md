# FEATURE: Rate Loading

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Validates and atomically loads ECB CSV history into the rates database. |
| Depends On  | DATABASE.md, ARCHITECTURE.md |
| Provides    | fxrates load |
| Consumes    | rates.list, rates.upsert |

## Purpose

Load a supplied ECB history CSV into the configured database while the application is running or stopped. Validate the whole file before its first write so a rejected file leaves every existing rate unchanged.

## Trigger and Workflow

The CLI accepts `fxrates load <csv>`. The loader reads the CSV, validates its header and all rows, then upserts each non-`N/A` rate by `(date, currency)`. It ignores one trailing empty CSV field on each line. A successful load reports the number of distinct dates that contain at least one rate and the number of rates stored from the file. A failure writes no standard output and one diagnostic line to standard error.

Header requirements: first field `Date`; remaining fields are three-letter uppercase currency codes. Each row has one date and one value per currency. Dates must be real `YYYY-MM-DD` calendar dates and unique within the file. Values are either `N/A` or nonzero values matching `[0-9]+(\.[0-9]+)?`. Wrong row width, malformed or repeated date, missing value, zero, or malformed rate rejects the whole file with exit code 3. An unreadable file is an operational failure with exit code 1.

## Database Interface

- `FEATURE-RATE-001` — read: list rates by optional date and currency - supplies: `date`, `currency` - returns: `id`, `date`, `currency`, `rate`
- `FEATURE-RATE-002` — write: replace a rate by date and currency - supplies: `date`, `currency`, `rate` - returns: `id`, `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC load-valid-file ===
Intent: A valid staged ECB file loads successfully and stores its published rate text.

from cli.testing import cli_runner
from persistence.testing import db_session

code, _, _ = cli_runner("init")
assert code == 0
code, _, _ = cli_runner("load", "sources/eurofxref-hist_2025-01.csv")
assert code == 0

with db_session() as db:
    rows = db.rates.list(date="2025-01-17", currency="USD")
    assert len(rows) == 1
    assert rows[0].rate == "1.0298"
=== END AC load-valid-file ===

=== AC load-rejection-atomic ===
Intent: A rejected file returns the declared status and leaves previously stored rates intact.

from cli.testing import cli_runner
from persistence.testing import db_session

code, _, _ = cli_runner("load", "sources/eurofxref-hist_2025-01.csv")
assert code == 0
with db_session() as db:
    before = db.rates.list(date="2025-01-31", currency="USD")
    assert len(before) == 1

code, _, _ = cli_runner("load", "sources/eurofxref-hist_bad.csv")
assert code == 3
with db_session() as db:
    after = db.rates.list(date="2025-01-31", currency="USD")
    assert len(after) == 1
    assert after[0].rate == before[0].rate
=== END AC load-rejection-atomic ===

=== AC load-replacement ===
Intent: Loading a valid file again replaces matching rates without creating duplicates.

from cli.testing import cli_runner
from persistence.testing import db_session

code, _, _ = cli_runner("load", "sources/eurofxref-hist_2025-01.csv")
assert code == 0
code, _, _ = cli_runner("load", "sources/eurofxref-hist_2025-01.csv")
assert code == 0

with db_session() as db:
    rows = db.rates.list(date="2025-01-29", currency="CHF")
    assert len(rows) == 1
    assert rows[0].rate == "0.943"
=== END AC load-replacement ===

## User Acceptance

- None.

## Guardrails

- Validate the full input file before the first database write.
- Do not convert published rate text to floating point.
- Do not change stored rows when any part of the file is rejected.
