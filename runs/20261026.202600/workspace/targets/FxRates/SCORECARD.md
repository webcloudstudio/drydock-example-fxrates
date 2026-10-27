# Scorecard: FxRates

## Specification

> **NOT YET RUN**
> drydock score spec FxRates

## Acceptance

> **FAILED**
> drydock score ac FxRates · 2026-10-26T21:18:56.520+00:00

PASS 29   FAIL 3   UNVERIFIED 0   PREPASSED 1   (33 AC total)

Failed:
- init-clears-store — FEATURE-Init.md
- latest-rates-empty — FEATURE-LatestRates.md
- stats-empty-store — FEATURE-Stats.md

## Build

> **RECORDED**
> drydock score build FxRates

Blocks: 6   Repaired: 3   Failed: 0
Tokens: 3,804,305 (cached 3,392,768, output 29,641)   Cache hit rate: 89.9%

## Release

> **RELEASED**
> drydock score release FxRates · 2026-10-26T21:20:36.381+00:00

- Verdict: PASSED

FxRates: PASSED — 10 of 10

  st-001  MET       ["sh", "sources/run.sh"] exited 0; sources/run.sh: outcome PASS, return code 0, 35 passed and 0 failed
  st-002  MET       bin/test.sh:1 uses #!/bin/sh; offline command: sh bin/test.sh exited 0; 29 passed
  st-003  MET       services/rates.py: load_file parses rows before writing and stores values through upsert; persistence/schema.py: rates.upsert matches on date and currency; probe: replacement preserved '2.00' and other rates; invalid input left stored rows unchanged; sources/run.sh: A4 passed with expected exit 3
  st-004  MET       app_server/main.py: health returns {'status':'ok'}; probe: GET /health returned 200 with {'status': 'ok'}
  st-005  MET       sources/run.sh: H5 and L4 passed for dates after a publication; sources/run.sh: H6 and H16 passed with 404 when no earlier publication exists; app_server/main.py: effective uses publications_through
  st-006  MET       sources/run.sh: H9–H12 and H17–H18 passed; app_server/main.py: conversion and history calculations use Decimal and ROUND_HALF_EVEN
  st-007  MET       sources/run.sh: H7, H13–H15, H16, and H21 passed with their expected statuses; app_server/main.py: request validation raises HTTPException with the specified statuses
  st-008  MET       services/rates.py: database access uses open_database(database_dsn()); config/__init__.py: database_dsn selects DATABASE_URL; persistence/schema.py: rates.upsert accepts and returns rate as str; services/rates.py: load_file passes the published rate string to upsert; application modules contain no direct database driver access
  st-009  MET       ["unshare", "-rn", "sh", "bin/test.sh"] exited 0; offline command: unshare -rn sh bin/test.sh exited 0; 29 passed
  st-010  MET       tests/test_fetch.py: success test patches urllib.request.urlopen and asserts loaded rates; tests/test_fetch.py: failure test patches urlopen to raise OSError and asserts exit code 1; offline command: test suite passed

## Project acceptance

| ID | Type | Criterion | Verdict | Observed |
|---|---|---|---|---|
| st-001 | technical | The completed fxrates shall make sh sources/run.sh exit zero; that script's exit status is the sole acceptance verdict. | MET | ["sh", "sources/run.sh"] exited 0; sources/run.sh: outcome PASS, return code 0, 35 passed and 0 failed |
| st-002 | technical | The application shall provide a POSIX-compatible bin/test.sh that exits zero when every automated test passes. | MET | bin/test.sh:1 uses #!/bin/sh; offline command: sh bin/test.sh exited 0; 29 passed |
| st-003 | behavioral | When an ECB history file is loaded, the application shall store every non-N/A rate as published text, replace rates already stored for the same date and currency, and, if any row is invalid, exit 3 and store nothing. | MET | services/rates.py: load_file parses rows before writing and stores values through upsert; persistence/schema.py: rates.upsert matches on date and currency; probe: replacement preserved '2.00' and other rates; invalid input left stored rows unchanged; sources/run.sh: A4 passed with expected exit 3 |
| st-004 | technical | When fxrates serve --port is run, the application shall answer GET /health on 127.0.0.1 at that port with status 200 and {"status": "ok"}. | MET | app_server/main.py: health returns {'status':'ok'}; probe: GET /health returned 200 with {'status': 'ok'} |
| st-005 | behavioral | When rates or a conversion are requested for a date, the application shall use the latest publication date on or before it, and respond 404 when there is none. | MET | sources/run.sh: H5 and L4 passed for dates after a publication; sources/run.sh: H6 and H16 passed with 404 when no earlier publication exists; app_server/main.py: effective uses publications_through |
| st-006 | behavioral | The application shall compute /convert rates and results and /history statistics with exact decimal arithmetic rounded half to even, matching the known answers in sources/run.sh. | MET | sources/run.sh: H9–H12 and H17–H18 passed; app_server/main.py: conversion and history calculations use Decimal and ROUND_HALF_EVEN |
| st-007 | behavioral | If a request has a malformed date or amount or lacks a required parameter, then the application shall respond 422; if it names an unknown currency, then it shall respond 404. | MET | sources/run.sh: H7, H13–H15, H16, and H21 passed with their expected statuses; app_server/main.py: request validation raises HTTPException with the specified statuses |
| st-008 | technical | The application shall reach the database only through the shipped persistence library, selected by DATABASE_URL, with rates stored as text and never as floating point. | MET | services/rates.py: database access uses open_database(database_dsn()); config/__init__.py: database_dsn selects DATABASE_URL; persistence/schema.py: rates.upsert accepts and returns rate as str; services/rates.py: load_file passes the published rate string to upsert; application modules contain no direct database driver access |
| st-009 | technical | The application's bin/test.sh shall exit zero when run with network access denied. | MET | ["unshare", "-rn", "sh", "bin/test.sh"] exited 0; offline command: unshare -rn sh bin/test.sh exited 0; 29 passed |
| st-010 | technical | The application's automated tests shall run fetch against a stubbed download, covering a successful load and a failed download that exits 1. | MET | tests/test_fetch.py: success test patches urllib.request.urlopen and asserts loaded rates; tests/test_fetch.py: failure test patches urlopen to raise OSError and asserts exit code 1; offline command: test suite passed |

**Material decisions:**

- Application module boundaries — 
- Repository operation surface — 
