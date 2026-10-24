# FEATURE: CLI Load

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Specifies validation and atomic loading of ECB history CSV files. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | fxrates load |
| Consumes    | rates persistence operations |

## Purpose

`fxrates load <csv>` validates the complete file before writing, then inserts or replaces all eligible rates.

## CSV Rules

- The first header field is `Date`; remaining fields are three-letter uppercase currency codes. Ignore the trailing empty field produced by the ECB trailing comma.
- Each data row contains one valid real date in `YYYY-MM-DD` form and one value per header currency. Dates cannot repeat within the file.
- `N/A` means no rate and creates no stored row. Every other value must match `[0-9]+(\.[0-9]+)?` and be nonzero.
- A wrong field count, invalid or repeated date, or invalid rate rejects the entire file before any write.
- Loading an existing `(date, currency)` replaces that rate. Repeating a successful load leaves the store unchanged.

On success, stdout is CSV with header `dates,rates` and the number of dates with at least one stored rate plus the number of rates stored from that file. A read failure exits `1`; a rejected file exits `3`. Failures write nothing to stdout and one diagnostic line to stderr.

## Programmatic Acceptance

=== AC load-valid-file ===
Intent: A valid staged ECB file loads successfully and reports its parsed counts.

import csv
import subprocess
import sys
from pathlib import Path

fixture = Path("sources/eurofxref-hist_2025-01.csv")
with fixture.open(newline="") as source:
    rows = list(csv.reader(source))
dates = {row[0] for row in rows[1:] if row[0]}
rate_count = sum(
    1 for row in rows[1:] if row[0]
    for value in row[1:] if value and value != "N/A"
)
result = subprocess.run(
    ["./fxrates", "load", str(fixture)],
    capture_output=True, text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
assert dates
assert rate_count
=== END AC load-valid-file ===

=== AC load-rejected-file-is-atomic ===
Intent: A rejected staged file returns the declared rejection status without changing stored rates.

import subprocess
import sys
from pathlib import Path
from persistence.testing import db_session

fixture = Path("sources/eurofxref-hist_bad.csv")
with db_session() as db:
    before = db.rates.list_all()
result = subprocess.run(
    ["./fxrates", "load", str(fixture)],
    capture_output=True, text=True,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 3
with db_session() as db:
    after = db.rates.list_all()
assert len(after) == len(before)
=== END AC load-rejected-file-is-atomic ===
