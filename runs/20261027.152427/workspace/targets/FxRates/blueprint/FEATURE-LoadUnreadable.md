# FEATURE: Load Unreadable File

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | A missing or unreadable file makes `fxrates load` exit 1 with one stderr line and write nothing. |
| Depends On | FEATURE-LoadStore.md |
| Provides | fxrates load unreadable-file handling |
| Consumes | fxrates load |

## Purpose

Operational failures reading the input file are distinct from a rejected file. An `OSError` (missing
file, directory, permission) or undecodable content while reading makes `load` exit `1`, print
nothing to standard output, write exactly one diagnostic line to standard error, and write nothing
to the database.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC load-missing-file ===
Intent: Loading a path that does not exist exits 1 with empty stdout and one stderr line, and adds no rows.
Requires: executable=python3; scope=test

import os
import tempfile
from persistence.testing import db_session
from cli.testing import cli_runner

with db_session() as db:
    before = len(db.rates.list_all_keys())
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "no-such-file.csv")
        code, out, err = cli_runner("load", path)
    assert code == 1
    assert out == ""
    assert len(err.splitlines()) == 1
    assert len(db.rates.list_all_keys()) == before
=== END AC load-missing-file ===

=== AC load-directory-path ===
Intent: Loading a directory cannot be read as a file, so it exits 1 with empty stdout and one stderr line.
Requires: executable=python3; scope=test

import tempfile
from persistence.testing import db_session
from cli.testing import cli_runner

with db_session() as db:
    before = len(db.rates.list_all_keys())
    with tempfile.TemporaryDirectory() as tmp:
        code, out, err = cli_runner("load", tmp)
    assert code == 1
    assert out == ""
    assert len(err.splitlines()) == 1
    assert len(db.rates.list_all_keys()) == before
=== END AC load-directory-path ===

=== AC load-undecodable-file ===
Intent: A file whose bytes are not valid text exits 1 with empty stdout and one stderr line, and stores nothing.
Requires: executable=python3; scope=test

import os
import tempfile
from persistence.testing import db_session
from cli.testing import cli_runner

with db_session() as db:
    before = len(db.rates.list_all_keys())
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "binary.csv")
        with open(path, "wb") as fh:
            fh.write(b"\xff\xfe\xfa\x80\x81\xff")
        code, out, err = cli_runner("load", path)
    assert code == 1
    assert out == ""
    assert len(err.splitlines()) == 1
    assert len(db.rates.list_all_keys()) == before
=== END AC load-undecodable-file ===

## User Acceptance

- None.

## Guardrails

- An unreadable file is exit 1 and never exit 3; exit 3 is reserved for a rejected file.
- Nothing is written to the database when the file cannot be read.
