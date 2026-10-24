# MANIFEST: FxRates
updated:     2026-10-24T07:38:44+00:00
state:       approved
blocks:      3

## story 1: Establish the Python application, FastAPI server, CLI, and generated SQLite persistence foundations.
id:           foundation
finding: programmatic acceptance failed: app-factory, architecture-boundary: persistence verification failed: persistence artifacts missing; rebuild the DATABASE step
evidence: evidence/block-1.md
summary:      Establish the Python application, FastAPI server, CLI, and generated SQLite persistence foundations.
type:         foundational
kind:         capability
phase:        1
block:        1
implements:   ARCHITECTURE.md
instructions: |
  Establish the application structure and integrate the selected foundations: Python 3.11+, FastAPI with uvicorn, the root fxrates executable, and SQLite through the shipped persistence package. Keep database access behind the generated persistence contract. Follow the module ownership and runtime configuration boundaries in ARCHITECTURE.md.
stack:        common.md, python.md, fastapi.md, sqlite.md, cli.md
stack_mode:   builder
size:         8872
provides:     app_server.create_app, cli.main, persistence.open_database
acceptance:   yes
state: closed/failed

## story 2: Declare the rates table and repository operations required by loading and API features.
id:           data_schema
summary:      Declare the rates table and repository operations required by loading and API features.
type:         foundational
kind:         capability
phase:        1
block:        2
implements:   DATABASE.md
instructions: |
  Declare the rates schema and typed repository operations used by file loading and API queries. Keep the natural key on date and currency, store published rates as text, and cover every declared operation with its own database-session acceptance check.
stack:        python.md, sqlite.md, persistence.md
stack_mode:   builder
size:         8862
provides:     rates.list, rates.upsert
consumes:     persistence.open_database
depends:      foundation
acceptance:   yes
state:        pending

## story 3: Validate and atomically load ECB history CSV files with replacement and reporting.
id: data_load
summary: Validate and atomically load ECB history CSV files with replacement and reporting.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Rate-Loading.md
covers: DATA-001, DATA-002
accepts: st-003
context: eurofxref-hist_2025-01.csv, eurofxref-hist_bad.csv, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, cli.md, sqlite.md
stack_mode: consumer
size: 10047
provides: fxrates load
consumes: rates.upsert, rates.list
instructions: Implement fxrates load. Parse and validate the complete file before writing any rows. Ignore a trailing empty CSV field, skip N/A rates, reject malformed or repeated dates and malformed, zero, or missing rates with exit code 3, and leave storage unchanged on rejection. Replace matching date and currency rows on success. Report date and rate counts to stdout in the specified two-line format; failures write no stdout and one diagnostic line to stderr.
acceptance: yes
depends: data_schema, foundation
state: pending

## story 4: Serve health, database statistics, currencies, and the API reference.
id: api_overview
summary: Serve health, database statistics, currencies, and the API reference.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-Overview.md
covers: API-001
accepts: st-004
context: eurofxref-hist_2025-01.csv, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md, sqlite.md
stack_mode: consumer
size: 8674
provides: GET /health, GET /stats, GET /currencies, GET /docs
consumes: rates.list
instructions: Implement health, statistics, sorted currency listing, and the FastAPI API reference entry point. Derive all statistics and currency values from persisted rates. Return null first and last dates when the table is empty.
acceptance: yes
depends: data_schema, foundation
state: pending

## story 5: Retrieve effective-date and latest publication rates.
id: api_rates
summary: Retrieve effective-date and latest publication rates.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Rate-Queries.md
covers: API-002
accepts: st-005, st-007
context: eurofxref-hist_2025-01.csv, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md, sqlite.md
stack_mode: consumer
size: 8701
provides: GET /rates/{date}, GET /rates/latest
consumes: rates.list
instructions: Implement date and latest rate retrieval from persisted data. Resolve a date to the latest publication on or before it; return 404 when no publication is available. Return 422 for malformed dates.
acceptance: yes
depends: data_schema, foundation
state: pending

## story 6: Convert currency amounts using exact Decimal arithmetic and half-even rounding.
id: api_conversion
summary: Convert currency amounts using exact Decimal arithmetic and half-even rounding.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Currency-Conversion.md
covers: API-003
accepts: st-006, st-007
context: eurofxref-hist_2025-01.csv, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md, sqlite.md
stack_mode: consumer
size: 8784
provides: GET /convert
consumes: rates.list
instructions: Implement conversion for EUR and stored currencies. Validate required parameters, date, and amount; return 422 for malformed or missing inputs and 404 for unavailable publication dates or currencies. Compute from unrounded stored rates using Decimal and round the displayed conversion rate to six places and result to two places, both half-even.
acceptance: yes
depends: data_schema, foundation
state: pending

## story 7: Return currency history and exact date-range statistics.
id: api_history
summary: Return currency history and exact date-range statistics.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Currency-History.md
covers: API-004
accepts: st-006, st-007
context: eurofxref-hist_2025-01.csv, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md, sqlite.md
stack_mode: consumer
size: 8890
provides: GET /history/{code}
consumes: rates.list
instructions: Implement ascending history points with optional inclusive start and end dates. Return stored text for points and extrema, and calculate the mean using Decimal rounded half-even to six places. Return empty-range statistics with null extrema and mean; return 404 for a currency without stored rates and 422 for malformed bounds.
acceptance: yes
depends: data_schema, foundation
state: pending

## story 8: Download the ECB history archive and load its CSV using the shared loader.
id: data_fetch
summary: Download the ECB history archive and load its CSV using the shared loader.
type: service
kind: integration
phase: 1
block: 3
implements: FEATURE-Rate-Fetch.md
covers: DATA-003
accepts: st-009
context: eurofxref-hist_2025-01.csv, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, cli.md
stack_mode: consumer
size: 7684
provides: fxrates fetch
consumes: fxrates.load
instructions: Implement fxrates fetch by downloading the documented ECB ZIP archive, extracting eurofxref-hist.csv, and passing its contents through the same validation, atomic persistence, and reporting behavior as load. Make the download replaceable in tests so fetch tests use a stub and open no network connection.
acceptance: yes
depends: data_load, foundation
state: pending

## story 9: Provide the fxrates executable, subcommands, help, and usage and operational error handling.
id: cli_interface
summary: Provide the fxrates executable, subcommands, help, and usage and operational error handling.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-CLI.md
covers: CLI-001
accepts: st-002
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, cli.md
stack_mode: consumer
size: 7625
provides: fxrates init, fxrates load, fxrates fetch, fxrates serve
consumes: cli.main
instructions: Implement the executable command interface and documented arguments, command help, and exit codes. Coordinate command dispatch with the load and fetch implementations. Initialization drops and recreates the rates table through the declared persistence boundary. Serve runs the API on 127.0.0.1 and shuts down cleanly on SIGTERM.
acceptance: yes
depends: foundation
state: pending

## story 10: Provide the project pytest suite and POSIX test launcher for all commands, endpoints, validation, arithmetic, and stubbed fetch behavior.
id: project_tests
summary: Provide the project pytest suite and POSIX test launcher for all commands, endpoints, validation, arithmetic, and stubbed fetch behavior.
type: service
kind: test harness
phase: 1
block: 3
implements: FEATURE-Test-Suite.md
accepts: st-002, st-009
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, pytest.md
stack_mode: builder
size: 6013
provides: bin/test.sh, pytest suite
instructions: Create bin/test.sh and a pytest suite covering each command, load validation and atomicity, every endpoint, effective-date selection, rounding, errors, and fetch through a stubbed download. Tests must not open a network connection.
acceptance: yes
depends: data_load, data_fetch, cli_interface, api_overview, api_rates, api_conversion, api_history, foundation
state: pending

## story 11: Run the supplied conformance grader as the terminal project verification gate.
id: full_verification
summary: Run the supplied conformance grader as the terminal project verification gate.
type: service
kind: test harness
phase: 1
block: 3
implements: VERIFICATION.md
covers: VERIFY-001
accepts: st-001
context: run.sh, eurofxref-hist_2025-01.csv, eurofxref-hist_2025-02-03_04.csv, eurofxref-hist_bad.csv
stack: common.md, python.md
stack_mode: consumer
size: 5661
instructions: Run the supplied sources/run.sh from the completed application root and require its exit status to be zero. This is the sole full-suite verification story and runs after all implementation stories.
acceptance: yes
depends: data_load, cli_interface, api_overview, api_rates, api_conversion, api_history, data_fetch
state: pending
