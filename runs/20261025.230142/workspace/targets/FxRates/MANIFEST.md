# MANIFEST: FxRates
updated: 2026-10-25T23:07:50+00:00
state: approved
blocks:      3

applied_specs: |
  ARCHITECTURE.md sha256=3c1ba416c40fca4ccb89d71893212a371cc5e15e1734eecb354bc3418c93aabd commit=0d49d9debb9da769d5a23e82e592347f7de39e84 applied_by=block-1 applied_at=2026-10-25T23:11:56+00:00 build_sha256=a61788c14b2fd7a5b24f0248248d104d95cb363c95b60de0b5991f6451f923c0

## story 1: Define application modules and their ownership boundaries.
id:           architecture
finding: ADVISORY: implemented, not verified — no governed acceptance command covers this story. Declare one in ACCEPTANCE.json to gate it.
evidence: evidence/block-1.md
summary:      Define application modules and their ownership boundaries.
type:         foundational
kind:         capability
phase:        1
block:        1
implements:   ARCHITECTURE.md
instructions: |
  Define the application structure and ownership boundaries for configuration, CLI, API,
  services, and persistence. Application code reaches SQLite only through the generated
  persistence package.
stack:        python.md
stack_mode:   builder
size:         2212
provides:     application module boundaries
acceptance:   yes
state: closed/implemented

## story 2: Declare the rates store and repository operations.
id:           database
finding: programmatic acceptance failed: rates_list_filters_and_order: AssertionError
evidence: evidence/block-2.md
summary:      Declare the rates store and repository operations.
type:         foundational
kind:         capability
phase:        1
block:        2
implements:   DATABASE.md
instructions: |
  Declare the rates table and every repository operation required for initialization,
  loading, and API reads, including effective-date lookup, currency history, counts,
  and rate replacement.
stack:        persistence.md, sqlite.md
stack_mode:   builder
size:         9489
provides:     rates repository operations
acceptance:   yes
state: closed/failed

## story 3: Provide the FastAPI application foundation.
id: api-foundation
finding: step block-2 failed: rates_list_filters_and_order
evidence: evidence/block-2.md
summary: Provide the FastAPI application foundation.
type: foundational
kind: capability
phase: 1
block: 2
implements: FEATURE-ApiFoundation.md
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, python.md
stack_mode: builder
size: 4837
provides: app_server.main:create_app, app_server.main:app
instructions: |
  Establish the FastAPI application factory and module-level application using the
  published app_server foundation contract.
acceptance: yes
depends: architecture, database
state: closed/failed

## story 4: Provide the executable command-line foundation.
id: cli-foundation
finding: step block-2 failed: rates_list_filters_and_order
evidence: evidence/block-2.md
summary: Provide the executable command-line foundation.
type: foundational
kind: capability
phase: 1
block: 2
implements: FEATURE-CliFoundation.md
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md, python.md
stack_mode: builder
size: 6022
provides: ./fxrates command entry point
instructions: |
  Establish the root executable and CLI entry point with the selected command-line
  foundation contract.
acceptance: yes
depends: architecture
state: closed/failed

## story 5: Initialize the rates store from the command line.
id: load_init
summary: Initialize the rates store from the command line.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-InitializeRates.md
covers: LOAD-001
accepts: st-008
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md, python.md, sqlite.md
stack_mode: consumer
size: 8075
provides: fxrates init
consumes: rates repository operations
instructions: |
  Implement fxrates init so it drops and recreates the rates table empty using the
  declared persistence boundary. Match the specified success, usage, and operational
  behavior.
acceptance: yes
depends: cli-foundation, database
state: pending

## story 6: Validate and atomically load ECB history files.
id: load_history
summary: Validate and atomically load ECB history files.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-LoadHistory.md
covers: LOAD-002
accepts: st-003, st-008
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md, python.md, sqlite.md
stack_mode: consumer
size: 8606
provides: fxrates load
consumes: rates repository operations
instructions: |
  Implement complete-file validation before writes, preserve published rate text, skip
  N/A values, replace duplicate stored date and currency pairs, and report stored dates
  and rates. Follow the specified exit codes and diagnostic channel.
acceptance: yes
depends: load_init
state: pending

## story 7: Serve health, statistics, and available currencies.
id: api_reference
summary: Serve health, statistics, and available currencies.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-ApiReference.md
covers: API-001
accepts: st-004, st-008
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, python.md, sqlite.md
stack_mode: consumer
size: 6957
provides: GET /health, GET /stats, GET /currencies
consumes: rates repository operations
instructions: |
  Implement health, database statistics, and ascending currency reference responses
  using the declared repository interface.
acceptance: yes
depends: api-foundation, database
state: pending

## story 8: Retrieve rates for effective and latest publication dates.
id: api_rates
summary: Retrieve rates for effective and latest publication dates.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-EffectiveRates.md
covers: API-002
accepts: st-005, st-008
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, python.md, sqlite.md
stack_mode: consumer
size: 7076
provides: GET /rates/{date}, GET /rates/latest
consumes: rates repository operations
instructions: |
  Resolve requests to the latest publication on or before the requested date and return
  the rates for that publication. Return 404 when no publication is available.
acceptance: yes
depends: api-foundation, database
state: pending

## story 9: Convert amounts between currencies.
id: api_convert
summary: Convert amounts between currencies.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Convert.md
covers: API-003
accepts: st-006, st-008
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, python.md, sqlite.md
stack_mode: consumer
size: 7194
provides: GET /convert
consumes: rates repository operations
instructions: |
  Implement exact Decimal conversion, effective-date resolution, half-even rounding,
  and the specified formatted values and errors.
acceptance: yes
depends: api-foundation, database
state: pending

## story 10: Retrieve currency history and statistics.
id: api_history
summary: Retrieve currency history and statistics.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-CurrencyHistory.md
covers: API-004
accepts: st-006, st-008
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, python.md, sqlite.md
stack_mode: consumer
size: 7326
provides: GET /history/{code}
consumes: rates repository operations
instructions: |
  Return ordered history points within optional inclusive bounds, with count, extrema,
  and exact Decimal mean rounded half to even.
acceptance: yes
depends: api-foundation, database
state: pending

## story 11: Start the API on the configured local port.
id: api_serve
summary: Start the API on the configured local port.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Serve.md
covers: API-006
accepts: st-004
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md, fastapi.md, python.md
stack_mode: consumer
size: 6794
provides: fxrates serve
consumes: app_server.main:app
instructions: |
  Implement foreground uvicorn serving on 127.0.0.1, accepting the requested port or
  defaulting to 8000 and stopping cleanly on SIGTERM.
acceptance: yes
depends: cli-foundation, api-foundation
state: pending

## story 12: Fetch and load the ECB history archive.
id: load_fetch
summary: Fetch and load the ECB history archive.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-FetchHistory.md
covers: LOAD-003
accepts: st-009
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md, python.md
stack_mode: consumer
size: 6266
provides: fxrates fetch
consumes: fxrates load
instructions: |
  Download and extract the ECB history archive, then pass its CSV through the shared
  loader. Keep automated fetch tests network-free by replacing the download with a stub.
acceptance: yes
depends: load_history
state: pending

## story 13: Validate API inputs and return specified errors.
id: api_errors
summary: Validate API inputs and return specified errors.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-ApiErrors.md
covers: API-005
accepts: st-007
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, python.md
stack_mode: consumer
size: 5428
provides: API request validation and error responses
consumes: GET /rates/{date}, GET /convert, GET /history/{code}
instructions: |
  Ensure malformed dates and amounts and missing required parameters return 422,
  while unknown or unavailable currencies and dates return 404.
acceptance: yes
depends: api-foundation, api_rates, api_convert, api_history
state: pending

## story 14: Verify the completed application against the supplied release gates.
id: release_verification
summary: Verify the completed application against the supplied release gates.
type: service
kind: test harness
phase: 1
block: 3
implements: VERIFICATION.md
accepts: st-001, st-002
context: run.sh, INSTRUCTIONS.md
stack: common.md, python.md
stack_mode: builder
size: 8135
instructions: |
  Provide the project test launcher and run the supplied grader and project test suite
  as the final verification after all implementation stories are complete. The supplied
  grader's exit status is the conformance verdict.
acceptance: yes
depends: load_init, load_history, load_fetch, api_reference, api_rates, api_convert, api_history, api_errors, api_serve
state: pending
