# Scorecard: FxRates

## Specification

> **NOT YET RUN**
> drydock score spec FxRates

## Acceptance

> **PASSED**
> drydock score ac FxRates · 2026-10-24T17:58:47.363+00:00

PASS 28   FAIL 0   UNVERIFIED 0   PREPASSED 5   (33 AC total)

## Build

> **RECORDED**
> drydock score build FxRates

Blocks: 3   Repaired: 1   Failed: 0
Tokens: 2,406,861 (cached 2,202,496, output 14,398)   Cache hit rate: 92.1%

## Release

> **FAILED**
> drydock score release FxRates · 2026-10-24T18:01:05.988+00:00

- Verdict: FAILED

FxRates: FAILED — 8 of 9

  st-001  MET       ["sh", "sources/run.sh"] exited 0; sources/run.sh: outcome PASS, return code 0; sources/run.sh output: FxRates: 35 passed, 0 failed (of 35)
  st-002  MET       bin/test.sh: POSIX shell script invoking pytest; bin/test.sh: 1 passed, 0 failed
  st-003  MET       services/common.py: load_csv_text parses all rows before upserting rates; probe: loaded 1.23450, skipped N/A, replaced it with 9.8700, and invalid input stored nothing
  st-004  MET       sources/run.sh: start_server waits for GET /health on 127.0.0.1; sources/run.sh output: PASS H1: GET /health
  st-005  MET       sources/run.sh output: PASS H4, H5, H6, L4
  st-006  MET       sources/run.sh output: PASS H9–H12 and H17–H18
  st-007  MET       sources/run.sh output: PASS H7, H13–H15, H21
  st-008  MET       services/common.py: imports open_database from persistence; cli/commands.py: imports open_database from persistence; persistence/schema.py: Rate.rate is str; schema.sql: rates.rate is TEXT NOT NULL; persistence/db.py: selects the driver from the DSN
  st-009  NOT MET   tests/test_architecture_imports.py: tests importability only; rg search: no test references fetch, urlopen stubbing, or network blocking

## Project acceptance

| ID | Type | Criterion | Verdict | Observed |
|---|---|---|---|---|
| st-001 | technical | The completed fxrates shall make sh sources/run.sh exit zero; that script's exit status is the sole acceptance verdict. | MET | ["sh", "sources/run.sh"] exited 0; sources/run.sh: outcome PASS, return code 0; sources/run.sh output: FxRates: 35 passed, 0 failed (of 35) |
| st-002 | technical | The application shall provide a POSIX-compatible bin/test.sh that exits zero when every automated test passes. | MET | bin/test.sh: POSIX shell script invoking pytest; bin/test.sh: 1 passed, 0 failed |
| st-003 | behavioral | When an ECB history file is loaded, the application shall store every non-N/A rate as published text, replace rates already stored for the same date and currency, and, if any row is invalid, exit 3 and store nothing. | MET | services/common.py: load_csv_text parses all rows before upserting rates; probe: loaded 1.23450, skipped N/A, replaced it with 9.8700, and invalid input stored nothing |
| st-004 | technical | When fxrates serve --port is run, the application shall answer GET /health on 127.0.0.1 at that port with status 200 and {"status": "ok"}. | MET | sources/run.sh: start_server waits for GET /health on 127.0.0.1; sources/run.sh output: PASS H1: GET /health |
| st-005 | behavioral | When rates or a conversion are requested for a date, the application shall use the latest publication date on or before it, and respond 404 when there is none. | MET | sources/run.sh output: PASS H4, H5, H6, L4 |
| st-006 | behavioral | The application shall compute /convert rates and results and /history statistics with exact decimal arithmetic rounded half to even, matching the known answers in sources/run.sh. | MET | sources/run.sh output: PASS H9–H12 and H17–H18 |
| st-007 | behavioral | If a request has a malformed date or amount or lacks a required parameter, then the application shall respond 422; if it names an unknown currency, then it shall respond 404. | MET | sources/run.sh output: PASS H7, H13–H15, H21 |
| st-008 | technical | The application shall reach the database only through the shipped persistence library, selected by DATABASE_URL, with rates stored as text and never as floating point. | MET | services/common.py: imports open_database from persistence; cli/commands.py: imports open_database from persistence; persistence/schema.py: Rate.rate is str; schema.sql: rates.rate is TEXT NOT NULL; persistence/db.py: selects the driver from the DSN |
| st-009 | technical | The application's automated tests shall exercise fetch through a stubbed download and shall not open a network connection. | NOT MET | tests/test_architecture_imports.py: tests importability only; rg search: no test references fetch, urlopen stubbing, or network blocking |

**Failures:**
- st-009 is NOT MET: The application's automated tests shall exercise fetch through a stubbed download and shall not open a network connection.

**Ranked improvements:**
1. Resolve st-009 (NOT MET): The application's automated tests shall exercise fetch through a stubbed download and shall not open a network connection.
2. Add an automated fetch test that stubs the download and verifies no network connection is opened.

**Material decisions:**

- Shared project foundation — 
