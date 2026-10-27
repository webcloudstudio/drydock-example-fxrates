# FEATURE: Fetch

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Implement fxrates fetch, which downloads the ECB history zip, extracts the CSV and loads it exactly as load does, testable with a stubbed download. |
| Depends On | FEATURE-LoadSummary.md, FEATURE-EcbParse.md |
| Provides | fxrates fetch |
| Consumes | fxrates load summary output, ecb.parse_history |

## Purpose

`fxrates fetch` retrieves the ECB's published history file and loads it with the same validation, atomicity, storage and summary as `fxrates load`.

## Interface

- `ecb.download_history() -> str` performs the whole download. It calls `urllib.request.urlopen("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip", timeout=...)` through the module attribute, reads the bytes inside a `with` block, opens them with `zipfile`, and returns the decoded text of the member `eurofxref-hist.csv`.
- Any failure (network error, non-zip data, missing member) raises `OperationalError` (exit 1).
- `cli/commands/fetch.py` `run(args)` calls `ecb.download_history()` through the module attribute `ecb`, so tests can replace it, then runs the same parse, store and summary path as `load` on that text (sharing a text-level helper with `load`). It takes no arguments.
- Exit codes follow `load`: 0 success, 1 download failure, 3 rejected file. Failures write nothing to stdout and one diagnostic line to stderr.
- Automated tests never open a network connection: they replace `ecb.download_history`, or replace `urllib.request.urlopen`.

## Database Interface

- None — storage is reached through the shared load path.

## Programmatic Acceptance

=== AC fetch-stubbed-download-loads ===
Intent: With the download replaced by a stub returning valid CSV text, fetch exits 0, prints the load summary, and stores the rates as published.
Requires: executable=python3; scope=test

import csv
import io
from unittest import mock
from cli.testing import cli_runner
from persistence.testing import db_session

d1, d2 = "1800-08-01", "1800-08-02"
header = ["Date", "ZZA", "ZZB", ""]
rows = [[d1, "1.20", "N/A", ""], [d2, "3.5", "4.25", ""]]
buf = io.StringIO()
writer = csv.writer(buf, lineterminator="\n")
writer.writerow(header)
for row in rows:
    writer.writerow(row)
text = buf.getvalue()

with mock.patch("ecb.download_history", return_value=text):
    code, out, err = cli_runner("fetch")
print(out, err)
assert code == 0
rate_count = sum(1 for row in rows for i in (1, 2) if row[i] != "N/A")
parsed = list(csv.reader(io.StringIO(out)))
assert parsed == [["dates", "rates"], [str(len(rows)), str(rate_count)]]

with db_session() as db:
    for i in (1, 2):
        back = db.rates.history(currency=header[i], start_date=d1, end_date=d2)
        want = sorted((row[0], row[i]) for row in rows if row[i] != "N/A")
        assert [(r.date, r.rate) for r in back] == want
=== END AC fetch-stubbed-download-loads ===

=== AC fetch-failed-download-exits-1 ===
Intent: When the download raises a network error, fetch exits 1, prints nothing to stdout, writes one stderr line, and stores nothing.
Requires: executable=python3; scope=test

import urllib.error
import urllib.request
from unittest import mock
from cli.testing import cli_runner
from persistence.testing import db_session

with db_session() as db:
    before = len(db.rates.list_all())

with mock.patch(
    "urllib.request.urlopen", side_effect=urllib.error.URLError("stubbed failure")
):
    code, out, err = cli_runner("fetch")
print(out, err)
assert code == 1
assert out == ""
assert len(err.strip().splitlines()) == 1

with db_session() as db:
    assert len(db.rates.list_all()) == before
=== END AC fetch-failed-download-exits-1 ===

=== AC fetch-zip-extraction ===
Intent: With only the HTTP call replaced, fetch extracts eurofxref-hist.csv from the zip and loads it, while a zip lacking that member exits 1.
Requires: executable=python3; scope=test

import csv
import io
import zipfile
from unittest import mock
from cli.testing import cli_runner
from persistence.testing import db_session


class FakeResponse:
    def __init__(self, data):
        self._data = data

    def read(self, *args):
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def make_zip(member, text):
    raw = io.BytesIO()
    with zipfile.ZipFile(raw, "w") as zf:
        zf.writestr(member, text)
    return raw.getvalue()


d = "1800-08-10"
header = ["Date", "ZZA", ""]
row = [d, "6.75", ""]
buf = io.StringIO()
writer = csv.writer(buf, lineterminator="\n")
writer.writerow(header)
writer.writerow(row)
text = buf.getvalue()

good = FakeResponse(make_zip("eurofxref-hist.csv", text))
with mock.patch("urllib.request.urlopen", return_value=good):
    code, out, err = cli_runner("fetch")
print(out, err)
assert code == 0
with db_session() as db:
    back = db.rates.history(currency="ZZA", start_date=d, end_date=d)
    assert [(r.date, r.rate) for r in back] == [(d, row[1])]

wrong = FakeResponse(make_zip("other.csv", text))
with mock.patch("urllib.request.urlopen", return_value=wrong):
    code, out, err = cli_runner("fetch")
assert code == 1
assert out == ""
=== END AC fetch-zip-extraction ===

=== AC fetch-rejected-file ===
Intent: A downloaded file with an invalid value exits 3 with empty stdout and stores nothing, as load does.
Requires: executable=python3; scope=test

import csv
import io
from unittest import mock
from cli.testing import cli_runner
from persistence.testing import db_session

d_ok, d_bad = "1800-08-21", "1800-08-20"
header = ["Date", "ZZA", ""]
rows = [[d_ok, "1.5", ""], [d_bad, "oops", ""]]
buf = io.StringIO()
writer = csv.writer(buf, lineterminator="\n")
writer.writerow(header)
for row in rows:
    writer.writerow(row)

with mock.patch("ecb.download_history", return_value=buf.getvalue()):
    code, out, err = cli_runner("fetch")
print(out, err)
assert code == 3
assert out == ""

with db_session() as db:
    assert db.rates.history(currency="ZZA", start_date=d_bad, end_date=d_ok) == []
=== END AC fetch-rejected-file ===

## User Acceptance

- None.

## Guardrails

- No automated test opens a network connection; the download is always stubbed.
- `fetch` loads through the same validated, atomic path as `load`.
- Downloaded content is treated as untrusted input and is never executed or written outside the store.
