# FEATURE: Load ECB History

| Field | Value |
|-------|-------|
| Version | 20261024 V1 |
| Description | Defines validation, atomic loading, and reporting for ECB CSV history files. |
| Depends On | FEATURE-CLI.md, DATABASE.md |
| Provides | fxrates load |
| Consumes | rates.upsert |

## Purpose

`./fxrates load <csv>` validates the complete input before writing, then stores every non-`N/A` rate as the exact published text. A matching `(date, currency)` replaces the stored rate. Successful output is CSV with header `dates,rates` and counts for dates containing at least one stored rate and rates stored from this file.

## Validation and Failure Behavior

- The first header field is `Date`; remaining fields are three-letter uppercase currency codes. Ignore a trailing empty field.
- Every row has a real `YYYY-MM-DD` date, unique within the file, and the expected number of fields.
- Values are `N/A` or nonzero strings matching `[0-9]+(\.[0-9]+)?`.
- Any invalid row rejects the entire file with exit 3 and no database changes.
- An unreadable file is an operational failure with exit 1.
- Failures write no stdout and one diagnostic line to stderr.

## Programmatic Acceptance

=== AC load-valid-fixture ===
Intent: The supplied valid January fixture loads successfully and reports its declared date and rate counts.
Cite: sources/INSTRUCTIONS.md:8-10
Cite: sources/run.sh:86-94

import csv
import io
import subprocess

result = subprocess.run(
    ["./fxrates", "load", "sources/eurofxref-hist_2025-01.csv"],
    capture_output=True,
    text=True,
)
assert result.returncode == 0
rows = list(csv.reader(io.StringIO(result.stdout)))
assert rows[0] == ["dates", "rates"]
assert rows[1] == ["22", "176"]
=== END AC load-valid-fixture ===

=== AC load-invalid-atomic ===
Intent: The supplied malformed fixture is rejected with exit 3.
Cite: sources/INSTRUCTIONS.md:39-42
Cite: sources/run.sh:95-95

import subprocess

result = subprocess.run(
    ["./fxrates", "load", "sources/eurofxref-hist_bad.csv"],
    capture_output=True,
    text=True,
)
assert result.returncode == 3
assert result.stdout == ""
=== END AC load-invalid-atomic ===

=== AC load-repeat ===
Intent: Loading the same valid file twice succeeds and reports the same file counts both times.
Cite: sources/run.sh:86-94

import csv
import io
import subprocess

def load():
    return subprocess.run(
        ["./fxrates", "load", "sources/eurofxref-hist_2025-01.csv"],
        capture_output=True,
        text=True,
    )

first = load()
second = load()
assert first.returncode == 0
assert second.returncode == 0
assert list(csv.reader(io.StringIO(first.stdout))) == list(csv.reader(io.StringIO(second.stdout)))
=== END AC load-repeat ===

## User Acceptance

- None.

## Guardrails

- Validate the entire file before the first write.
- Preserve rate text exactly; never convert stored rates to floating point.
- Do not modify any file under `sources/`.

## Database Interface

- `FEATURE-DATA-001` — write: rates.upsert - supplies: `date`, `currency`, `rate` - returns: `date`, `currency`, `rate`
