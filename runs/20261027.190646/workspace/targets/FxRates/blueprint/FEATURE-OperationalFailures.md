# FEATURE: Operational Failures

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Proves that an unreadable load file and a failed fetch download each exit 1 with one stderr line, empty stdout and an unchanged database. |
| Depends On | FEATURE-LoadAtomic.md, FEATURE-Fetch.md, FEATURE-CliFoundation.md |
| Provides | fxrates exit code 1 diagnostics |
| Consumes | fxrates load, fxrates fetch |

## Purpose

Operational failures are exit code `1`: a `load` file that cannot be read, and a `fetch` download that fails. This story assembles `load` and `fetch` and proves the seams between them and the dispatcher. Each failure writes nothing to standard output, writes exactly one diagnostic line to standard error, and leaves stored rates untouched. Any seam that breaks this is fixed here.

## Behavior

| Trigger | Exit | Stdout | Stderr | Database |
|---------|------|--------|--------|----------|
| `fxrates load <path>` where `<path>` does not exist or cannot be read | 1 | empty | one line | unchanged |
| `fxrates fetch` where `ecb.download_history()` raises `OperationalError` | 1 | empty | one line | unchanged |

Tests replace `ecb.download_history` with a stub; no test opens a network connection.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC failures-load-unreadable ===
Intent: Loading a path that does not exist exits 1 with empty stdout and exactly one stderr line, and the stored rates are the same before and after.
Requires: executable=python3; scope=test

import os
import tempfile
from cli.testing import cli_runner
from persistence.testing import db_session

with tempfile.TemporaryDirectory() as tmp:
    missing = os.path.join(tmp, "no-such-file.csv")
    with db_session() as db:
        before = [(r.date, r.currency, r.rate) for r in db.rates.list_all()]
        code, out, err = cli_runner("load", missing)
        assert code == 1
        assert out == ""
        assert len(err.strip().splitlines()) == 1
        after = [(r.date, r.currency, r.rate) for r in db.rates.list_all()]
        assert after == before
=== END AC failures-load-unreadable ===

=== AC failures-load-directory ===
Intent: Loading a path that is a directory is also unreadable and exits 1 with empty stdout, leaving stored rates unchanged.
Requires: executable=python3; scope=test

import tempfile
from cli.testing import cli_runner
from persistence.testing import db_session

with tempfile.TemporaryDirectory() as tmp:
    with db_session() as db:
        before = [(r.date, r.currency, r.rate) for r in db.rates.list_all()]
        code, out, err = cli_runner("load", tmp)
        assert code == 1
        assert out == ""
        assert len(err.strip().splitlines()) == 1
        after = [(r.date, r.currency, r.rate) for r in db.rates.list_all()]
        assert after == before
=== END AC failures-load-directory ===

=== AC failures-fetch-download ===
Intent: When the stubbed download raises OperationalError, fetch exits 1 with empty stdout and one stderr line, and stored rates are unchanged.
Requires: executable=python3; scope=test

import ecb
from cli.testing import cli_runner
from persistence.testing import db_session

try:
    from cli.errors import OperationalError
except ImportError:
    from cli import OperationalError


def failing_download():
    raise OperationalError("download failed")


original = ecb.download_history
ecb.download_history = failing_download
try:
    with db_session() as db:
        before = [(r.date, r.currency, r.rate) for r in db.rates.list_all()]
        code, out, err = cli_runner("fetch")
        assert code == 1
        assert out == ""
        assert len(err.strip().splitlines()) == 1
        after = [(r.date, r.currency, r.rate) for r in db.rates.list_all()]
        assert after == before
finally:
    ecb.download_history = original
=== END AC failures-fetch-download ===

## User Acceptance

- None.

## Guardrails

- A failing command writes nothing to standard output.
- A failing command writes exactly one diagnostic line to standard error.
- No test opens a network connection; the download is always stubbed.
- A failure never deletes or alters stored rates.
