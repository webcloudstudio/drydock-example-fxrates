# FEATURE: Load Visibility

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | A completed load is visible to the next API request, and a rejected load changes nothing a request can see. |
| Depends On | FEATURE-LoadStore.md, FEATURE-Stats.md, DATABASE.md |
| Provides | load visibility contract |
| Consumes | fxrates load, GET /stats |

## Purpose

Loads happen while the server runs. This integration story proves the API reads committed state on every request and that a load is applied as one transaction.

## Behavior

- The API opens its store per request and caches no rows or connection state that could hide a later commit.
- `load` validates the whole file, then writes inside one transaction, so a reader sees the rates from before the load or from after it, never part of it.
- A rejected load (exit 3) leaves `/stats` unchanged.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC load-visible-to-stats ===
Intent: After a successful load of one new date with two currencies, /stats reports one more date and two more rates than before, and last equals the loaded date.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

import csv
import os
import tempfile
from cli.testing import cli_runner
from app_server.testing import web_client

d = "2999-12-30"
rows = [["Date", "ZZA", "ZZB", ""], [d, "1.5", "2.25", ""]]

client = web_client()
before = client.get("/stats")
assert before.status_code == 200
b = before.json()

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "load.csv")
    with open(path, "w", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerows(rows)
    code, out, err = cli_runner("load", path)
    assert code == 0

after = client.get("/stats")
assert after.status_code == 200
a = after.json()
assert a["dates"] == b["dates"] + 1
assert a["rates"] == b["rates"] + 2
assert a["last"] == d
=== END AC load-visible-to-stats ===

=== AC rejected-load-invisible ===
Intent: A file whose second row holds an invalid value is rejected with exit 3 and /stats is identical before and after.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

import csv
import os
import tempfile
from cli.testing import cli_runner
from app_server.testing import web_client

rows = [
    ["Date", "ZZA", ""],
    ["2999-11-02", "1.5", ""],
    ["2999-11-01", "1.5x", ""],
]

client = web_client()
before = client.get("/stats")
assert before.status_code == 200

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "bad.csv")
    with open(path, "w", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerows(rows)
    code, out, err = cli_runner("load", path)
    assert code == 3
    assert out == ""

after = client.get("/stats")
assert after.status_code == 200
assert after.json() == before.json()
=== END AC rejected-load-invisible ===

=== AC reload-leaves-stats ===
Intent: Loading the same file twice leaves /stats unchanged by the second load, because replaced rows are not added.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

import csv
import os
import tempfile
from cli.testing import cli_runner
from app_server.testing import web_client

rows = [["Date", "ZZA", ""], ["2999-10-01", "7.5", ""]]

client = web_client()
with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "again.csv")
    with open(path, "w", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerows(rows)
    code, out, err = cli_runner("load", path)
    assert code == 0
    first = client.get("/stats")
    assert first.status_code == 200
    code, out, err = cli_runner("load", path)
    assert code == 0
    second = client.get("/stats")
    assert second.status_code == 200
    assert second.json() == first.json()
=== END AC reload-leaves-stats ===

## User Acceptance

- None.

## Guardrails

- A load never leaves a partly applied state visible to a request.
- The API never caches stored rows between requests.
- A rejected file writes nothing.
