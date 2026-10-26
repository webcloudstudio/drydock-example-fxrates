# Scorecard: FxRates

## Specification

> **NOT YET RUN**
> drydock score spec FxRates

## Acceptance

> **FAILED**
> drydock score ac FxRates · 2026-10-26T01:31:55.296+00:00

PASS 14   FAIL 12   UNVERIFIED 0   PREPASSED 0   (26 AC total)

Failed:
- init-empty — FEATURE-DatabaseInitialization.md
- overview-routes — FEATURE-ServiceOverview.md
- stats-empty-contract — FEATURE-ServiceOverview.md
- effective-rate-routes — FEATURE-EffectiveRates.md
- effective-rate-errors — FEATURE-EffectiveRates.md
- history-route — FEATURE-CurrencyHistory.md
- history-summary-and-empty — FEATURE-CurrencyHistory.md
- history-errors — FEATURE-CurrencyHistory.md
- conversion-route — FEATURE-CurrencyConversion.md
- conversion-rounding — FEATURE-CurrencyConversion.md
- conversion-errors — FEATURE-CurrencyConversion.md
- fetch-operational-error — FEATURE-HistoryFetch.md

## Build

> **RECORDED**
> drydock score build FxRates

Blocks: 3   Repaired: 0   Failed: 0
Tokens: 1,094,829 (cached 1,009,536, output 6,788)   Cache hit rate: 92.8%

## Release

> **FAILED**
> drydock score release FxRates · 2026-10-26T01:33:22.726+00:00

- Verdict: FAILED

FxRates: FAILED — 8 of 9

  st-001  MET       ["sh", "sources/run.sh"] exited 0; governed gate: sh sources/run.sh exited 0; governed gate output: FxRates: 35 passed, 0 failed (of 35)
  st-002  MET       bin/test.sh: executable POSIX shell script; sh bin/test.sh: exit 0, 1 passed
  st-003  MET       services/loader.py: load_text parses before opening the database and upserts each parsed rate; .drydock-probe/loader_probe.py: passed text preservation, replacement, and atomic invalid-load checks
  st-004  MET       app_server/main.py: /health returns {"status":"ok"}; sources/run.sh: starts fxrates serve and checks /health; governed gate: PASS H1: GET /health
  st-005  MET       app_server/main.py: rates_for uses effective(requested) and raises 404 when no rates are selected; governed gate: PASS H5 for 2025-01-18 resolving to 2025-01-17; PASS H6 for 2024-12-31 returning 404
  st-006  MET       app_server/main.py: conversion and history calculations use Decimal; services/queries.py: decfmt quantizes with ROUND_HALF_EVEN; governed gate: PASS H9-H12 conversions and PASS H17-H18 history statistics
  st-007  MET       app_server/main.py: malformed dates and amounts raise HTTP 422; unknown currencies raise HTTP 404; governed gate: PASS H7, H13-H16, H21
  st-008  MET       services/loader.py and services/queries.py: database access goes through persistence.open_database; config.py: DATABASE_URL is the first database-location setting; schema.sql: rates.rate is TEXT NOT NULL; persistence/schema.py: rate fields are typed as str
  st-009  NOT MET   tests/test_architecture_imports.py: only test_architecture_entry_points_are_importable is defined; services/fetch.py: fetch calls download_archive, but no automated test stubs or calls it

## Project acceptance

| ID | Type | Criterion | Verdict | Observed |
|---|---|---|---|---|
| st-001 | technical | The completed fxrates shall make sh sources/run.sh exit zero; that script's exit status is the sole acceptance verdict. | MET | ["sh", "sources/run.sh"] exited 0; governed gate: sh sources/run.sh exited 0; governed gate output: FxRates: 35 passed, 0 failed (of 35) |
| st-002 | technical | The application shall provide a POSIX-compatible bin/test.sh that exits zero when every automated test passes. | MET | bin/test.sh: executable POSIX shell script; sh bin/test.sh: exit 0, 1 passed |
| st-003 | behavioral | When an ECB history file is loaded, the application shall store every non-N/A rate as published text, replace rates already stored for the same date and currency, and, if any row is invalid, exit 3 and store nothing. | MET | services/loader.py: load_text parses before opening the database and upserts each parsed rate; .drydock-probe/loader_probe.py: passed text preservation, replacement, and atomic invalid-load checks |
| st-004 | technical | When fxrates serve --port is run, the application shall answer GET /health on 127.0.0.1 at that port with status 200 and {"status": "ok"}. | MET | app_server/main.py: /health returns {"status":"ok"}; sources/run.sh: starts fxrates serve and checks /health; governed gate: PASS H1: GET /health |
| st-005 | behavioral | When rates or a conversion are requested for a date, the application shall use the latest publication date on or before it, and respond 404 when there is none. | MET | app_server/main.py: rates_for uses effective(requested) and raises 404 when no rates are selected; governed gate: PASS H5 for 2025-01-18 resolving to 2025-01-17; PASS H6 for 2024-12-31 returning 404 |
| st-006 | behavioral | The application shall compute /convert rates and results and /history statistics with exact decimal arithmetic rounded half to even, matching the known answers in sources/run.sh. | MET | app_server/main.py: conversion and history calculations use Decimal; services/queries.py: decfmt quantizes with ROUND_HALF_EVEN; governed gate: PASS H9-H12 conversions and PASS H17-H18 history statistics |
| st-007 | behavioral | If a request has a malformed date or amount or lacks a required parameter, then the application shall respond 422; if it names an unknown currency, then it shall respond 404. | MET | app_server/main.py: malformed dates and amounts raise HTTP 422; unknown currencies raise HTTP 404; governed gate: PASS H7, H13-H16, H21 |
| st-008 | technical | The application shall reach the database only through the shipped persistence library, selected by DATABASE_URL, with rates stored as text and never as floating point. | MET | services/loader.py and services/queries.py: database access goes through persistence.open_database; config.py: DATABASE_URL is the first database-location setting; schema.sql: rates.rate is TEXT NOT NULL; persistence/schema.py: rate fields are typed as str |
| st-009 | technical | The application's automated tests shall exercise fetch through a stubbed download and shall not open a network connection. | NOT MET | tests/test_architecture_imports.py: only test_architecture_entry_points_are_importable is defined; services/fetch.py: fetch calls download_archive, but no automated test stubs or calls it |

**Failures:**
- st-009 is NOT MET: The application's automated tests shall exercise fetch through a stubbed download and shall not open a network connection.

**Ranked improvements:**
1. Resolve st-009 (NOT MET): The application's automated tests shall exercise fetch through a stubbed download and shall not open a network connection.
2. Add an automated test that stubs services.fetch.download_archive, exercises fetch, and verifies no network connection is opened.

**Material decisions:**

- Date count for loading reports — 
- Conversion result precision — 
- Empty history statistics — 
