# MANIFEST: FxRates
updated: 2026-10-24T16:00:42+00:00
state: draft
blocks:      3

## story 1: Establish application boundaries and shared module ownership.
id:           architecture-foundation
summary:      Establish application boundaries and shared module ownership.
type:         foundational
kind:         capability
phase:        1
block:        1
implements:   ARCHITECTURE.md
instructions: |
  Establish the Python application structure and document configuration, service, and persistence
  ownership boundaries. Application persistence access must use the shipped persistence library.
stack:        python.md
stack_mode:   builder
size:         2169
provides:     application module boundaries
acceptance:   yes
state:        pending

## story 2: Declare the rates store and its repository contract.
id:           database
summary:      Declare the rates store and its repository contract.
type:         foundational
kind:         capability
phase:        1
block:        2
implements:   DATABASE.md
instructions: |
  Declare the rates table and every repository operation required for initialization, atomic file
  loading, statistics, currency listing, effective-date lookup, conversion, and history. Rates
  remain published text and all application access uses the generated persistence package.
stack:        persistence.md, sqlite.md
stack_mode:   builder
size:         10180
provides:     rates repository operations
depends:      architecture-foundation
acceptance:   yes
state:        pending

## story 3: Establish the FastAPI application and test client.
id: api-foundation
summary: Establish the FastAPI application and test client.
type: foundational
kind: capability
phase: 1
block: 2
implements: FEATURE-API-FOUNDATION.md
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md
stack_mode: builder
size: 5399
provides: app_server.main:create_app, app_server.testing:web_client
instructions: |
  Establish the FastAPI application factory, module-level app, and callable TestClient helper
  required by API capabilities. Do not implement endpoint behavior owned by API stories.
acceptance: yes
depends: architecture-foundation
state: pending

## story 4: Establish the fxrates command-line entry point.
id: cli-foundation
summary: Establish the fxrates command-line entry point.
type: foundational
kind: capability
phase: 1
block: 2
implements: FEATURE-CLI.md
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md
stack_mode: builder
size: 6800
provides: fxrates executable, fxrates init, fxrates load, fxrates fetch, fxrates serve
consumes: rates repository operations
instructions: |
  Establish the root executable and command dispatch for init, load, fetch, and serve. Follow the
  source-defined usage, output, and exit-code contracts; command behavior is completed by the
  implementing stories.
acceptance: yes
depends: architecture-foundation, database
state: pending

## story 5: Initialize the rates database from the command line.
id: data_001
summary: Initialize the rates database from the command line.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-INIT.md
covers: DATA-001
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md, sqlite.md
stack_mode: consumer
size: 8596
provides: fxrates init
consumes: rates repository operations
instructions: |
  Implement init so it drops and recreates the rates table empty, prints nothing on success, and
  follows the specified usage and failure behavior.
acceptance: yes
depends: cli-foundation, database
state: pending

## story 6: Validate and atomically load ECB history files.
id: data_002
summary: Validate and atomically load ECB history files.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-LOAD.md
covers: DATA-002
accepts: st-003
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md, sqlite.md
stack_mode: consumer
size: 9024
provides: fxrates load
consumes: rates repository operations
instructions: |
  Validate the complete CSV before writing. Store valid non-N/A rates exactly as published,
  replace matching date and currency records, and report the counts defined by the source. Reject
  invalid files atomically with the specified exit code and diagnostic behavior.
acceptance: yes
depends: cli-foundation, database
state: pending

## story 7: List currencies present in stored rates.
id: api_002
summary: List currencies present in stored rates.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-CURRENCIES.md
covers: API-002
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, sqlite.md
stack_mode: consumer
size: 7596
provides: GET /currencies
consumes: rates repository operations
instructions: Return EUR as the base and currencies with stored rates in ascending order.
acceptance: yes
depends: api-foundation, database
state: pending

## story 8: Provide health and stored-data statistics endpoints.
id: api_001
summary: Provide health and stored-data statistics endpoints.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-STATUS.md
covers: API-001
accepts: st-004
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, sqlite.md
stack_mode: consumer
size: 7756
provides: GET /health, GET /stats
consumes: rates repository operations
instructions: Implement health and statistics responses, including null publication bounds for an empty store.
acceptance: yes
depends: api-foundation, database
state: pending

## story 9: Return currency history and summary statistics.
id: api_006
summary: Return currency history and summary statistics.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-HISTORY.md
covers: API-006
accepts: st-006, st-007, st-008
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, sqlite.md
stack_mode: consumer
size: 7934
provides: GET /history/{code}
consumes: rates repository operations
instructions: |
  Return ascending points within optional inclusive bounds, exact count, extrema, and the
  half-even rounded mean. Empty ranges return null statistics and no points. Return 404 for a
  currency with no stored rate, including EUR, and 422 for malformed bounds.
acceptance: yes
depends: api-foundation, database
state: pending

## story 10: Resolve and return rates for a requested date.
id: api_003
summary: Resolve and return rates for a requested date.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-RATES.md
covers: API-003, API-004
accepts: st-005, st-007
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, sqlite.md
stack_mode: consumer
size: 7944
provides: GET /rates/{date}, GET /rates/latest
consumes: rates repository operations
instructions: |
  Resolve requests to the latest publication date on or before the requested date. Return stored
  rate text, use the specified latest-request marker, return 404 when no publication exists, and
  return 422 for malformed dates.
acceptance: yes
depends: api-foundation, database
state: pending

## story 11: Convert amounts between currencies.
id: api_005
summary: Convert amounts between currencies.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-CONVERT.md
covers: API-005
accepts: st-005, st-006, st-007, st-008
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, sqlite.md
stack_mode: consumer
size: 8264
provides: GET /convert
consumes: rates repository operations
instructions: |
  Convert using the latest publication by default or the effective date requested. Use exact
  Decimal arithmetic with half-even rounding and the specified string formats. Return the required
  404 and 422 statuses for missing rates, unknown currencies, malformed values, and missing
  parameters.
acceptance: yes
depends: api-foundation, database
state: pending

## story 12: Fetch, extract, and load ECB history.
id: data_003
summary: Fetch, extract, and load ECB history.
type: service
kind: integration
phase: 1
block: 3
implements: FEATURE-FETCH.md
covers: DATA-003
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md
stack_mode: consumer
size: 6983
provides: fxrates fetch
consumes: fxrates load
instructions: |
  Download and extract the ECB history archive, then reuse the validated load behavior. Tests must
  stub the download. On download failure, return the specified operational failure signal with no
  standard output and one diagnostic line.
acceptance: yes
depends: cli-foundation, data_002
state: pending

## story 13: Provide a network-free automated pytest suite and runner.
id: test_001
summary: Provide a network-free automated pytest suite and runner.
type: service
kind: test harness
phase: 1
block: 3
implements: FEATURE-TESTS.md
covers: TEST-001
accepts: st-002, st-009
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md
stack_mode: consumer
size: 4914
provides: bin/test.sh, pytest suite
instructions: |
  Provide a POSIX-compatible runner for the project's pytest suite. Cover the commands, load
  rules, API endpoints, effective-date behavior, rounding, and error statuses using a real test
  database. Stub fetch so the suite never uses the network.
acceptance: yes
depends: cli-foundation, api-foundation, data_001, data_002, data_003, api_001, api_002, api_003, api_005, api_006
state: pending

## story 14: Verify the completed application against the supplied grader.
id: test_002
summary: Verify the completed application against the supplied grader.
type: service
kind: test harness
phase: 1
block: 3
implements: VERIFICATION.md
covers: TEST-002
accepts: st-001
context: run.sh, eurofxref-hist_2025-01.csv, eurofxref-hist_2025-02-03_04.csv, eurofxref-hist_bad.csv
stack: common.md, python.md
stack_mode: builder
size: 6371
instructions: |
  Run the complete supplied grader as the terminal verification gate after all implementation
  stories. Its exit status is the release acceptance verdict; do not duplicate its cases as
  hand-written assertions.
acceptance: yes
depends: test_001
state: pending
