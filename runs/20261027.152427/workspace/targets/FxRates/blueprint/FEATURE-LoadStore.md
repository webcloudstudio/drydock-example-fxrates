# FEATURE: Load Store

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | `fxrates load <csv>` validates an ECB history file, stores its rates as text in one transaction, and reports the dates and rates counts. |
| Depends On | FEATURE-LoadValidation.md, FEATURE-InitCommand.md, DATABASE.md |
| Provides | fxrates load |
| Consumes | fxrates_app.ecb.parse_history, rates.replace_rate, fxrates_app.config.database_path, cli.main |

## Purpose

`fxrates load <csv>` reads an ECB history file, validates it completely with
`fxrates_app.ecb.parse_history`, and then upserts every non-N/A rate through `rates.replace_rate`
in a single transaction, so a reader sees all or none of the load.

## Behavior

- A rejected file (`RejectedFile`) exits `3`, prints nothing to standard output, writes one
  diagnostic line to standard error, and stores nothing.
- On success it prints `dates,rates` on the first line and `<dates>,<rates>` on the second, where
  `dates` counts the dates in the file with at least one stored rate and `rates` counts the rates stored.
- A rate for a (date, currency) already stored replaces it, so loading the same file twice leaves the
  database unchanged.
- A file holding only N/A values prints `0,0` and stores nothing.
- Unreadable files are handled by FEATURE-LoadUnreadable.md.

## Database Interface

- `FEATURE-RATE-001` — write: store a rate, replacing the stored one - supplies: `date`, `currency`, `rate` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC load-counts-and-text ===
Intent: A valid file exits 0, reports the dates and rates counts derived from the fixture (an all-N/A date is not counted), and stores each rate as published text.
Requires: executable=python3; scope=test

import csv
import os
import tempfile
from persistence.testing import db_session
from cli.testing import cli_runner

header = ["Date", "ZZA", "ZZB", "ZZH"]
rows = [
    ["1900-08-03", "1.50", "N/A", "N/A"],
    ["1900-08-02", "0.943", "2", "N/A"],
    ["1900-08-01", "N/A", "N/A", "N/A"],
]
stored = [(r[0], c, v) for r in rows for c, v in zip(header[1:], r[1:]) if v != "N/A"]
n_dates = len({d for d, _, _ in stored})
n_rates = len(stored)

with db_session() as db:
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "in.csv")
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(header + [""])
            for r in rows:
                w.writerow(r + [""])
        code, out, err = cli_runner("load", path)
    assert code == 0
    lines = out.splitlines()
    assert lines[0] == "dates,rates"
    got_dates, got_rates = lines[1].split(",")
    assert int(got_dates) == n_dates
    assert int(got_rates) == n_rates
    assert len(lines) == 2
    for cur in header[1:]:
        hist = db.rates.list_currency_history(currency=cur)
        assert [(r.date, r.rate) for r in hist] == sorted((d, v) for d, c, v in stored if c == cur)
    assert db.rates.list_for_date(date="1900-08-01") == []
=== END AC load-counts-and-text ===

=== AC load-reload-is-idempotent ===
Intent: Loading the same file twice reports the same counts both times and leaves the stored rates unchanged.
Requires: executable=python3; scope=test

import csv
import os
import tempfile
from persistence.testing import db_session
from cli.testing import cli_runner

header = ["Date", "ZZA", "ZZB"]
rows = [["1900-08-12", "1.5", "2.5"], ["1900-08-11", "1.25", "N/A"]]

with db_session() as db:
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "in.csv")
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(header + [""])
            for r in rows:
                w.writerow(r + [""])
        code, out1, err = cli_runner("load", path)
        assert code == 0
        before = [(r.date, r.currency, r.rate) for c in header[1:] for r in db.rates.list_currency_history(currency=c)]
        code, out2, err = cli_runner("load", path)
        assert code == 0
        after = [(r.date, r.currency, r.rate) for c in header[1:] for r in db.rates.list_currency_history(currency=c)]
    assert out1 == out2
    assert before == after
    assert len(after) == sum(1 for r in rows for v in r[1:] if v != "N/A")
=== END AC load-reload-is-idempotent ===

=== AC load-replaces-existing-rate ===
Intent: A later file replaces a stored rate for the same date and currency, leaves other dates alone, and does not add a row.
Requires: executable=python3; scope=test

import csv
import os
import tempfile
from persistence.testing import db_session
from cli.testing import cli_runner

cur = "ZZA"
keep_date, swap_date = "1900-08-21", "1900-08-22"
old, new, other = "1.10", "9.9", "3.3"

def write(path, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["Date", cur, ""])
        for d, v in rows:
            w.writerow([d, v, ""])

with db_session() as db:
    with tempfile.TemporaryDirectory() as tmp:
        first = os.path.join(tmp, "a.csv")
        second = os.path.join(tmp, "b.csv")
        write(first, [(keep_date, other), (swap_date, old)])
        write(second, [(swap_date, new)])
        code, out, err = cli_runner("load", first)
        assert code == 0
        code, out, err = cli_runner("load", second)
        assert code == 0
    hist = db.rates.list_currency_history(currency=cur)
    assert [(r.date, r.rate) for r in hist] == [(keep_date, other), (swap_date, new)]
=== END AC load-replaces-existing-rate ===

=== AC load-rejected-file-changes-nothing ===
Intent: A file with a valid first row and an invalid later row exits 3 with empty stdout and one stderr line, and stores nothing, including the valid first row.
Requires: executable=python3; scope=test

import csv
import os
import tempfile
from persistence.testing import db_session
from cli.testing import cli_runner

cur = "ZZB"
good_date, bad_date = "1900-08-32"[:8] + "31", "1900-08-30"

with db_session() as db:
    before = len(db.rates.list_all_keys())
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "bad.csv")
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(["Date", cur, ""])
            w.writerow([good_date, "1.5", ""])
            w.writerow([bad_date, "1.0x", ""])
        code, out, err = cli_runner("load", path)
    assert code == 3
    assert out == ""
    assert len(err.splitlines()) == 1
    assert db.rates.list_currency_history(currency=cur) == []
    assert len(db.rates.list_all_keys()) == before
=== END AC load-rejected-file-changes-nothing ===

=== AC load-supplied-bad-file ===
Intent: The supplied bad ECB file is rejected with exit 3 and no rows are added.
Requires: executable=python3; scope=test

from persistence.testing import db_session
from cli.testing import cli_runner

with db_session() as db:
    before = len(db.rates.list_all_keys())
    code, out, err = cli_runner("load", "sources/eurofxref-hist_bad.csv")
    assert code == 3
    assert out == ""
    assert len(db.rates.list_all_keys()) == before
=== END AC load-supplied-bad-file ===

=== AC load-only-na ===
Intent: A file holding only N/A rates exits 0, reports zero dates and zero rates, and stores nothing.
Requires: executable=python3; scope=test

import csv
import os
import tempfile
from persistence.testing import db_session
from cli.testing import cli_runner

date = "1900-08-41"[:8] + "05"

with db_session() as db:
    before = len(db.rates.list_all_keys())
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "na.csv")
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(["Date", "ZZH", "ZZI", ""])
            w.writerow([date, "N/A", "N/A", ""])
        code, out, err = cli_runner("load", path)
    assert code == 0
    lines = out.splitlines()
    assert lines[0] == "dates,rates"
    assert [int(x) for x in lines[1].split(",")] == [0, 0]
    assert db.rates.list_for_date(date=date) == []
    assert len(db.rates.list_all_keys()) == before
=== END AC load-only-na ===

=== AC load-supplied-january-file ===
Intent: The supplied January file loads with counts derived from its own cells, and every stored USD rate equals the published text.
Requires: executable=python3; scope=test

import csv
from persistence.testing import db_session
from cli.testing import cli_runner

path = "sources/eurofxref-hist_2025-01.csv"
with open(path, newline="") as fh:
    table = list(csv.reader(fh))
codes = [h for h in table[0][1:] if h]
cells = []
for row in table[1:]:
    for code, value in zip(codes, row[1:1 + len(codes)]):
        if value != "N/A":
            cells.append((row[0], code, value))
n_dates = len({d for d, _, _ in cells})
n_rates = len(cells)

with db_session() as db:
    code, out, err = cli_runner("load", path)
    assert code == 0
    lines = out.splitlines()
    assert lines[0] == "dates,rates"
    assert [int(x) for x in lines[1].split(",")] == [n_dates, n_rates]
    hist = db.rates.list_currency_history(currency="USD")
    assert {r.date: r.rate for r in hist} == {d: v for d, c, v in cells if c == "USD"}
    assert db.rates.list_currency_history(currency="HRK") == []
=== END AC load-supplied-january-file ===

## User Acceptance

- None.

## Guardrails

- A rejected file changes nothing: the whole file is validated before the first write.
- The load is applied in one transaction so a reader never sees a partly applied load.
- Rates are stored as published text and arithmetic never uses floating point.
- Standard output carries only the counts; failures write one diagnostic line to standard error.
