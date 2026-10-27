# FEATURE: Fetch

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | `fxrates fetch` downloads the ECB history archive, extracts the CSV, and loads it through the validated load path. |
| Depends On | FEATURE-LoadStore.md, FEATURE-LoadUnreadable.md |
| Provides | fxrates fetch, fxrates_app.fetch.download_archive |
| Consumes | fxrates load, fxrates_app.ecb.parse_history |

## Purpose

`fxrates fetch` obtains the ECB euro reference rate history without a file argument. It downloads
`https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip`, extracts the member
`eurofxref-hist.csv`, and loads that text exactly as `fxrates load` does.

## Trigger

The command line: `./fxrates fetch`. It takes no arguments; a wrong argument count is a usage error
(exit 2) handled by the shared validation.

## Sequence

1. Call `fxrates_app.fetch.download_archive(url)` for the ECB URL. It returns the archive bytes and
   uses `urllib` with a builder-chosen timeout. It is the only function in the application that
   opens a network connection.
2. The handler must call it through the module attribute (`fxrates_app.fetch.download_archive(...)`),
   never through a name imported into another module, so tests replace the single seam.
3. Open the bytes as a zip archive and read the member `eurofxref-hist.csv`.
4. Pass its text through the same parse, validate, and transactional store path used by `load`
   (`fxrates_app.ecb.parse_history`, then one transaction of upserts).
5. Print `dates,rates` then `<dates>,<rates>`, as `load` does, and exit 0.

## Exit codes

| Condition | Exit | Stdout | Stderr | Stored |
|-----------|------|--------|--------|--------|
| Success | 0 | `dates,rates` then counts | diagnostics only | the rates |
| Download fails or times out | 1 | empty | one line | nothing |
| Bytes are not a zip archive | 1 | empty | one line | nothing |
| Archive lacks `eurofxref-hist.csv` | 1 | empty | one line | nothing |
| Member is a rejected file | 3 | empty | one line | nothing |

## Database Interface

- None — persistence is owned by DATABASE.md and reached through the load path.

## Programmatic Acceptance

=== AC fetch-loads-archive ===
Intent: With the download stubbed to return a zip holding the CSV, fetch exits 0, reports the date and rate counts, and stores each published rate text exactly.
Requires: executable=python3; scope=test

import csv
import io
import zipfile
from unittest import mock

from cli.testing import cli_runner
from persistence.testing import db_session

d = "1900-08-01"
ra = "1.50"
rb = "2.250"

buf = io.StringIO()
w = csv.writer(buf, lineterminator="\n")
w.writerow(["Date", "ZZA", "ZZB", ""])
w.writerow([d, ra, rb, ""])
text = buf.getvalue()

bio = io.BytesIO()
with zipfile.ZipFile(bio, "w") as z:
    z.writestr("eurofxref-hist.csv", text)
data = bio.getvalue()

with db_session() as db:
    with mock.patch("fxrates_app.fetch.download_archive", return_value=data):
        code, out, err = cli_runner("fetch")
    print(out)
    print(err)
    assert code == 0
    lines = out.splitlines()
    assert lines[0] == "dates,rates"
    assert lines[1].split(",") == [str(1), str(2)]
    rows = {r.currency: r.rate for r in db.rates.list_for_date(date=d)}
    assert rows["ZZA"] == ra
    assert rows["ZZB"] == rb
=== END AC fetch-loads-archive ===

=== AC fetch-download-failure ===
Intent: A failed download exits 1 with empty stdout and one stderr line, and stores nothing.
Requires: executable=python3; scope=test

from unittest import mock

from cli.testing import cli_runner
from persistence.testing import db_session

d = "1900-08-02"

with db_session() as db:
    before = db.rates.list_all_keys()
    with mock.patch("fxrates_app.fetch.download_archive", side_effect=OSError("network down")):
        code, out, err = cli_runner("fetch")
    assert code == 1
    assert out == ""
    assert len(err.strip().splitlines()) == 1
    assert db.rates.list_for_date(date=d) == []
    assert len(db.rates.list_all_keys()) == len(before)
=== END AC fetch-download-failure ===

=== AC fetch-bad-archive ===
Intent: Bytes that are not a zip archive, and a zip without eurofxref-hist.csv, each exit 1 with empty stdout and store nothing.
Requires: executable=python3; scope=test

import csv
import io
import zipfile
from unittest import mock

from cli.testing import cli_runner
from persistence.testing import db_session

d = "1900-08-03"

buf = io.StringIO()
w = csv.writer(buf, lineterminator="\n")
w.writerow(["Date", "ZZA", ""])
w.writerow([d, "1.5", ""])

bio = io.BytesIO()
with zipfile.ZipFile(bio, "w") as z:
    z.writestr("other.csv", buf.getvalue())
wrong_member = bio.getvalue()
not_a_zip = bytes(range(32))

with db_session() as db:
    before = len(db.rates.list_all_keys())
    for payload in (not_a_zip, wrong_member):
        with mock.patch("fxrates_app.fetch.download_archive", return_value=payload):
            code, out, err = cli_runner("fetch")
        assert code == 1
        assert out == ""
        assert len(err.strip().splitlines()) == 1
        assert db.rates.list_for_date(date=d) == []
    assert len(db.rates.list_all_keys()) == before
=== END AC fetch-bad-archive ===

=== AC fetch-rejected-member ===
Intent: A member that fails ECB validation exits 3 with empty stdout and writes nothing, even for rows preceding the invalid one.
Requires: executable=python3; scope=test

import csv
import io
import zipfile
from unittest import mock

from cli.testing import cli_runner
from persistence.testing import db_session

good = "1900-08-05"
bad = "1900-08-04"

buf = io.StringIO()
w = csv.writer(buf, lineterminator="\n")
w.writerow(["Date", "ZZA", ""])
w.writerow([good, "1.5", ""])
w.writerow([bad, "0", ""])

bio = io.BytesIO()
with zipfile.ZipFile(bio, "w") as z:
    z.writestr("eurofxref-hist.csv", buf.getvalue())
data = bio.getvalue()

with db_session() as db:
    with mock.patch("fxrates_app.fetch.download_archive", return_value=data):
        code, out, err = cli_runner("fetch")
    assert code == 3
    assert out == ""
    assert len(err.strip().splitlines()) == 1
    assert db.rates.list_for_date(date=good) == []
    assert db.rates.list_for_date(date=bad) == []
=== END AC fetch-rejected-member ===

## User Acceptance

- None.

## Guardrails

- No test opens a network connection; the download is replaced at `fxrates_app.fetch.download_archive`.
- A failing command writes nothing to standard output and one diagnostic line to standard error.
- Rates are stored as the ECB's published text and never as floating point.
- The timeout is builder-chosen because the sources state none.
