# FEATURE: Live Visibility

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Integration proof that a load completed while the application is running is visible to the next request. |
| Depends On | FEATURE-Serve.md, FEATURE-Stats.md, FEATURE-LoadSummary.md |
| Provides | live load visibility |
| Consumes | GET /stats, fxrates load, fxrates serve |

## Purpose

Assembly and intent: each request opens its own database handle through `persistence.open_database`, so a load committed after the app was created is reflected by the next `/stats` and `/rates/latest` request. Fix any seam that breaks this; no new interface is introduced.

## Routes

| Route | Role |
|-------|------|
| `GET /stats` | Counts and first/last dates reflect a load made after the app was created |
| `GET /rates/latest` | Latest publication reflects a load made after the app was created |

## Behavior

- The web client is created once, before the load; a long-lived connection or cached result would hide the load and fail this feature.
- Loading goes through the `load` command, not direct repository writes.
- Reloading changed rates replaces them and the next request shows the new values.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC live-load-visible-in-stats ===
Intent: A client created before a load sees the new dates and rates in /stats on the very next request, with counts that grow by exactly what the file contributed.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

import csv
import os
import tempfile
from app_server.testing import web_client
from cli.testing import cli_runner

dates = ["9998-12-30", "9998-12-31"]
currencies = ["ZZA", "ZZB"]
rates = {(d, c): f"{i + 1}.{j + 1}5" for i, d in enumerate(dates) for j, c in enumerate(currencies)}

client = web_client()
before_resp = client.get("/stats")
assert before_resp.status_code == 200
before = before_resp.json()
assert before["last"] != dates[-1]

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "live.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["Date", *currencies, ""])
        for d in dates:
            writer.writerow([d, *[rates[(d, c)] for c in currencies], ""])
    code, out, err = cli_runner("load", path)
    assert code == 0, err

after_resp = client.get("/stats")
assert after_resp.status_code == 200
after = after_resp.json()
assert after["dates"] == before["dates"] + len(dates)
assert after["rates"] == before["rates"] + len(rates)
assert after["last"] == max(dates)
=== END AC live-load-visible-in-stats ===

=== AC live-load-visible-in-rates ===
Intent: A load made after the client was created shows up as the latest publication with the loaded rate text, and the request before the load did not.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

import csv
import os
import tempfile
from app_server.testing import web_client
from cli.testing import cli_runner

date = "9998-12-29"
currency = "ZZL"
rate = "3.1400"

client = web_client()
before = client.get("/rates/latest")
assert before.status_code in (200, 404)
if before.status_code == 200:
    assert before.json()["date"] != date

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "live.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["Date", currency, ""])
        writer.writerow([date, rate, ""])
    code, out, err = cli_runner("load", path)
    assert code == 0, err

after = client.get("/rates/latest")
assert after.status_code == 200
body = after.json()
assert body["date"] == date
assert body["rates"][currency] == rate
=== END AC live-load-visible-in-rates ===

=== AC live-reload-replaces-visible ===
Intent: Reloading a file with a changed rate replaces the stored value and the next request returns the new text without changing the date count.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

import csv
import os
import tempfile
from app_server.testing import web_client
from cli.testing import cli_runner

date = "9998-12-28"
currency = "ZZR"
first, second = "1.5", "2.25"

def write_and_load(path, rate):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["Date", currency, ""])
        writer.writerow([date, rate, ""])
    code, out, err = cli_runner("load", path)
    assert code == 0, err

client = web_client()
with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "live.csv")
    write_and_load(path, first)
    mid = client.get("/stats")
    assert mid.status_code == 200
    mid_body = mid.json()
    seen = client.get("/rates/" + date)
    assert seen.status_code == 200
    assert seen.json()["rates"][currency] == first

    write_and_load(path, second)
    end = client.get("/stats")
    assert end.status_code == 200
    end_body = end.json()
    assert end_body["dates"] == mid_body["dates"]
    assert end_body["rates"] == mid_body["rates"]
    replaced = client.get("/rates/" + date)
    assert replaced.status_code == 200
    assert replaced.json()["rates"][currency] == second
=== END AC live-reload-replaces-visible ===

## User Acceptance

- None.

## Guardrails

- The app never caches rates or holds a long-lived database handle across requests.
- Application startup never initializes the schema; only `fxrates init` does.
- Acceptance loads through the `load` command interface, never by writing rows directly.
