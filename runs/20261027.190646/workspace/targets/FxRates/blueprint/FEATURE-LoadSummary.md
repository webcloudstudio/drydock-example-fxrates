# FEATURE: Load Summary

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Print the dates,rates summary on standard output after a successful load. |
| Depends On | FEATURE-LoadAtomic.md |
| Provides | fxrates load summary output |
| Consumes | fxrates load |

## Purpose

After a successful `fxrates load`, standard output reports how many dates and rates the file contributed to the store.

## Interface

- `cli/commands/load.py` `run(args)` prints, after `load_file` returns `(dates, rates)`, exactly two lines: `dates,rates` and then `<dates>,<rates>`, each newline-terminated.
- `dates` counts the dates in the file with at least one stored rate. A date whose values are all `N/A` is not counted.
- `rates` counts the rates stored from the file. These are counts from the file, not changes: loading the same file again prints the same numbers.
- On failure (exit 1, 2 or 3) nothing is written to standard output.

## Database Interface

- None — the counts come from `load_file`'s return value.

## Programmatic Acceptance

=== AC summary-counts ===
Intent: The first output line is dates,rates and the second carries the number of dates with a stored rate and the number of stored rates, derived from the fixture, with an all-N/A date not counted.
Requires: executable=python3; scope=test

import csv
import io
import os
import tempfile
from cli.testing import cli_runner

header = ["Date", "ZZA", "ZZB", "ZZC", ""]
rows = [
    ["1800-07-01", "1.1", "2.2", "N/A", ""],
    ["1800-07-02", "3.3", "N/A", "N/A", ""],
    ["1800-07-03", "N/A", "N/A", "N/A", ""],
]
values = [row[i] for row in rows for i in range(1, len(header) - 1)]
rate_count = sum(1 for v in values if v != "N/A")
date_count = sum(
    1 for row in rows if any(row[i] != "N/A" for i in range(1, len(header) - 1))
)

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "hist.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)

    code, out, err = cli_runner("load", path)
    print(out, err)
    assert code == 0
    assert out.endswith("\n")
    parsed = list(csv.reader(io.StringIO(out)))
    assert parsed == [["dates", "rates"], [str(date_count), str(rate_count)]]
=== END AC summary-counts ===

=== AC summary-repeat-load ===
Intent: Loading the same file twice prints the same counts both times because the summary counts what the file stored, not what changed.
Requires: executable=python3; scope=test

import csv
import io
import os
import tempfile
from cli.testing import cli_runner

header = ["Date", "ZZA", "ZZB", ""]
rows = [
    ["1800-07-11", "1.1", "2.2", ""],
    ["1800-07-12", "3.3", "4.4", ""],
]

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "hist.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)

    code1, out1, err1 = cli_runner("load", path)
    assert code1 == 0
    code2, out2, err2 = cli_runner("load", path)
    assert code2 == 0
    assert list(csv.reader(io.StringIO(out1))) == list(csv.reader(io.StringIO(out2)))
    parsed = list(csv.reader(io.StringIO(out2)))
    assert parsed[1] == [str(len(rows)), str(len(rows) * (len(header) - 2))]
=== END AC summary-repeat-load ===

=== AC summary-silent-on-failure ===
Intent: A rejected file and an unreadable file print nothing to standard output.
Requires: executable=python3; scope=test

import csv
import os
import tempfile
from cli.testing import cli_runner

header = ["Date", "ZZA", ""]
bad_rows = [["1800-07-21", "1.0x", ""]]

with tempfile.TemporaryDirectory() as tmp:
    bad = os.path.join(tmp, "bad.csv")
    with open(bad, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(header)
        for row in bad_rows:
            writer.writerow(row)

    code, out, err = cli_runner("load", bad)
    assert code == 3
    assert out == ""

    code, out, err = cli_runner("load", os.path.join(tmp, "missing.csv"))
    assert code == 1
    assert out == ""
=== END AC summary-silent-on-failure ===

## User Acceptance

- None.

## Guardrails

- The summary is exactly the header line and the counts line; nothing else is written to standard output.
- Diagnostics go to standard error only.
