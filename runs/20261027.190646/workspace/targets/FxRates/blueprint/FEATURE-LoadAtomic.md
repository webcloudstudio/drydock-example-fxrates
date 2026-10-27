# FEATURE: Atomic Load

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Implement fxrates load, which validates the whole ECB history file before its first write and stores nothing when the file is rejected. |
| Depends On | FEATURE-CliFoundation.md, FEATURE-Init.md, FEATURE-EcbParse.md, FEATURE-RateStorage.md |
| Provides | fxrates load |
| Consumes | ecb.parse_history, ratestore.store_rates, cli.main, fxrates init |

## Purpose

`fxrates load <csv>` loads an ECB history file into the store. The whole file is checked before the first write, so a rejected file changes nothing, and a rate already stored for the same date and currency is replaced.

## Interface

- `cli/commands/load.py` defines `load_file(path: str) -> tuple[int, int]` and `run(args) -> int`.
- `load_file` reads the file as UTF-8 text. A file that cannot be read raises `OperationalError` (exit 1).
- It calls `ecb.parse_history` on the full text. An invalid file raises `RejectedFile` (exit 3) before the database is opened for writing.
- It opens the store with `persistence.open_database(config.database_path())`, calls `ratestore.store_rates`, closes the database, and returns the `(dates, rates)` counts.
- `run` calls `load_file` and returns 0. Printing the summary is owned by FEATURE-LoadSummary.md; this story prints nothing to stdout on success.
- Failure output follows the dispatcher: nothing on stdout, one diagnostic line on stderr.

## Rules

1. Exit 0 on success, 1 when the file cannot be read, 3 when the file is rejected.
2. A rejected file leaves the database exactly as it was, including rows for dates the file shares with the store.
3. Loading the same file twice leaves the database unchanged.

## Database Interface

- None — persistence is reached through `ratestore.store_rates`.

## Programmatic Acceptance

=== AC load-stores-rates ===
Intent: Loading a valid file exits 0 and stores every non-N/A rate as published text, storing nothing for N/A values.
Requires: executable=python3; scope=test

import csv
import os
import tempfile
from cli.testing import cli_runner
from persistence.testing import db_session

d1, d2 = "1800-06-01", "1800-06-02"
header = ["Date", "ZZA", "ZZB", "ZZC", ""]
rows = [
    [d1, "1.2300", "5", "N/A", ""],
    [d2, "7.25", "N/A", "N/A", ""],
]

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

    with db_session() as db:
        for i in range(1, len(header) - 1):
            currency = header[i]
            rows_back = db.rates.history(currency=currency, start_date=d1, end_date=d2)
            got = [(r.date, r.rate) for r in rows_back]
            want = sorted((row[0], row[i]) for row in rows if row[i] != "N/A")
            assert got == want
=== END AC load-stores-rates ===

=== AC load-replaces-and-repeats ===
Intent: A rate already stored for a date and currency is replaced by the loaded text, and loading the same file a second time leaves the stored rows unchanged.
Requires: executable=python3; scope=test

import csv
import os
import tempfile
from cli.testing import cli_runner
from persistence.testing import db_session

d = "1800-06-10"
old = "1.0"
header = ["Date", "ZZA", "ZZB", ""]
row = [d, "3.14", "2.7", ""]

with db_session() as db:
    db.rates.replace_rate(date=d, currency="ZZA", rate=old)

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "hist.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(header)
        writer.writerow(row)

    code, out, err = cli_runner("load", path)
    assert code == 0
    with db_session() as db:
        snapshot = {}
        for i in (1, 2):
            rows_back = db.rates.history(currency=header[i], start_date=d, end_date=d)
            snapshot[header[i]] = [(r.date, r.rate) for r in rows_back]
            assert snapshot[header[i]] == [(d, row[i])]

    code, out, err = cli_runner("load", path)
    assert code == 0
    with db_session() as db:
        for i in (1, 2):
            rows_back = db.rates.history(currency=header[i], start_date=d, end_date=d)
            assert [(r.date, r.rate) for r in rows_back] == snapshot[header[i]]
=== END AC load-replaces-and-repeats ===

=== AC load-rejected-stores-nothing ===
Intent: A file whose first row is valid and whose second row has an invalid value exits 3, prints nothing to stdout, writes one stderr line, and leaves earlier stored rates and the valid row's date untouched.
Requires: executable=python3; scope=test

import csv
import os
import tempfile
from cli.testing import cli_runner
from persistence.testing import db_session

d_ok, d_bad = "1800-06-21", "1800-06-20"
keep_date, keep_rate = "1800-06-22", "4.4"
header = ["Date", "ZZA", "ZZB", ""]
rows = [
    [d_ok, "1.5", "2.5", ""],
    [d_bad, "1.0x", "2.5", ""],
]

with db_session() as db:
    db.rates.replace_rate(date=keep_date, currency="ZZA", rate=keep_rate)

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "bad.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)

    code, out, err = cli_runner("load", path)
    print(out, err)
    assert code == 3
    assert out == ""
    assert len(err.strip().splitlines()) == 1

    with db_session() as db:
        for currency in ("ZZA", "ZZB"):
            rows_back = db.rates.history(currency=currency, start_date=d_bad, end_date=d_ok)
            assert rows_back == []
        kept = db.rates.history(currency="ZZA", start_date=keep_date, end_date=keep_date)
        assert [(r.date, r.rate) for r in kept] == [(keep_date, keep_rate)]
=== END AC load-rejected-stores-nothing ===

=== AC load-unreadable-file ===
Intent: Loading a path that does not exist is an operational failure that exits 1 with empty stdout and one stderr line.
Requires: executable=python3; scope=test

import os
import tempfile
from cli.testing import cli_runner

with tempfile.TemporaryDirectory() as tmp:
    missing = os.path.join(tmp, "no-such-file.csv")
    code, out, err = cli_runner("load", missing)
    print(out, err)
    assert code == 1
    assert out == ""
    assert len(err.strip().splitlines()) == 1
=== END AC load-unreadable-file ===

## User Acceptance

- None.

## Guardrails

- The whole file is validated before the first write; a rejected file never changes the store.
- The command never initializes the schema; only `fxrates init` does.
- Application code opens the store only through `persistence.open_database`.
