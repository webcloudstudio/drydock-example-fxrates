# MANIFEST: FxRates
updated:     2026-10-25T01:44:40+00:00
state:       approved
blocks:      3

## story 1: Declare the rates schema and repository operations.
id:           database
summary:      Declare the rates schema and repository operations.
type:         foundational
kind:         capability
phase:        1
block:        1
implements:   DATABASE.md
instructions: |
  Declare the rates table and its repository operations for publication-date queries, currency queries, upserts, and deletion. Keep stored rates as text and use the generated persistence package for all database access.
stack:        persistence.md, sqlite.md
stack_mode:   builder
size:         9473
provides:     rates.get, rates.list, rates.upsert, rates.delete
acceptance:   yes
state:        pending

## story 2: Define application module boundaries and runtime wiring.
id:           architecture
summary:      Define application module boundaries and runtime wiring.
type:         foundational
kind:         capability
phase:        1
block:        2
implements:   ARCHITECTURE.md
instructions: |
  Establish the application structure, configuration resolution, FastAPI application factory, CLI entry point, and module boundaries. Route all database access through the shipped persistence library and keep fetch testable without network access.
stack:        python.md, fastapi.md, cli.md, sqlite.md
stack_mode:   builder
size:         7125
depends:      database
acceptance:   yes
state:        pending

## story 3: Initialize an empty rates database.
id: cli_init
summary: Initialize an empty rates database.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-CLI-INIT.md
covers: CLI-001
accepts: st-003
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, cli.md, sqlite.md
stack_mode: consumer
size: 8510
provides: fxrates init
instructions: Implement init so it drops and recreates the rates table, succeeds silently, and leaves an empty store.
acceptance: yes
depends: database, architecture
state: pending

## story 4: Validate and load ECB history files atomically and idempotently.
id: cli_load
summary: Validate and load ECB history files atomically and idempotently.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-CLI-LOAD.md
covers: CLI-002, CLI-004
accepts: st-003
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, cli.md, sqlite.md
stack_mode: consumer
size: 9028
provides: fxrates load
instructions: Implement complete-file validation before writes, preserve published rate text, omit N/A entries, replace existing date/currency rates, and report counts for dates with rates and stored rates.
acceptance: yes
depends: database, architecture
state: pending

## story 5: List the base currency and currencies with stored rates.
id: api_currencies
summary: List the base currency and currencies with stored rates.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-CURRENCIES.md
covers: API-002
accepts: st-008
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, fastapi.md, sqlite.md
stack_mode: consumer
size: 7160
provides: GET /currencies
instructions: Return EUR as base and stored currencies in ascending order.
acceptance: yes
depends: database, architecture
state: pending

## story 6: Serve health and database statistics.
id: api_health_stats
summary: Serve health and database statistics.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-HEALTH-STATS.md
covers: API-001
accepts: st-004
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, fastapi.md, sqlite.md
stack_mode: consumer
size: 7301
provides: GET /health, GET /stats
instructions: Implement JSON health and statistics endpoints, including empty-store behavior and date bounds.
acceptance: yes
depends: database, architecture
state: pending

## story 7: Resolve date-specific and latest effective rates.
id: api_rates
summary: Resolve date-specific and latest effective rates.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-RATES.md
covers: API-003
accepts: st-005
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, fastapi.md, sqlite.md
stack_mode: consumer
size: 7354
provides: GET /rates/{date}, GET /rates/latest
instructions: Resolve the latest publication on or before a requested date, return exact stored rate text, validate dates, and return 404 when no effective publication exists.
acceptance: yes
depends: database, architecture
state: pending

## story 8: Convert amounts between currencies with exact decimal arithmetic.
id: api_convert
summary: Convert amounts between currencies with exact decimal arithmetic.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-CONVERT.md
covers: API-004
accepts: st-006, st-007
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, fastapi.md, sqlite.md
stack_mode: consumer
size: 7724
provides: GET /convert
instructions: Validate required parameters and amounts, resolve the effective date, validate currency availability, and calculate rate and result using Decimal with half-even rounding.
acceptance: yes
depends: database, architecture
state: pending

## story 9: Retrieve bounded currency history and exact statistics.
id: api_history
summary: Retrieve bounded currency history and exact statistics.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-HISTORY.md
covers: API-005
accepts: st-005, st-006, st-007
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, fastapi.md, sqlite.md
stack_mode: consumer
size: 7828
provides: GET /history/{code}
instructions: Return ascending bounded publication points with stored text and exact min, max, and mean values; distinguish an empty bounded result from a currency with no stored rates.
acceptance: yes
depends: database, architecture
state: pending

## story 10: Fetch and load the ECB history archive.
id: cli_fetch
summary: Fetch and load the ECB history archive.
type: service
kind: integration
phase: 1
block: 3
implements: FEATURE-CLI-FETCH.md
covers: CLI-003
accepts: st-009
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, cli.md
stack_mode: consumer
size: 6724
provides: fxrates fetch
instructions: Download and extract the ECB archive and load its CSV through the same validation and persistence path as load. Keep automated tests fully stubbed from network access.
acceptance: yes
depends: cli_load, architecture
state: pending

## story 11: Expose API discovery documentation.
id: api_reference
summary: Expose API discovery documentation.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-REFERENCE.md
covers: API-003
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, fastapi.md
stack_mode: consumer
size: 5232
provides: GET /openapi.json
instructions: Expose the FastAPI OpenAPI document as the programmatic API discovery entry point.
acceptance: yes
depends: architecture
state: pending

## story 12: Provide the automated pytest suite and POSIX runner.
id: test_suite
summary: Provide the automated pytest suite and POSIX runner.
type: service
kind: test harness
phase: 1
block: 3
implements: FEATURE-TEST-SUITE.md
covers: TEST-001
accepts: st-002, st-009
context: run.sh, eurofxref-hist_2025-01.csv, eurofxref-hist_2025-02-03_04.csv, eurofxref-hist_bad.csv, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md
stack_mode: builder
size: 9457
instructions: Provide bin/test.sh and a pytest suite covering the command workflows, loading rules, API routes, effective-date resolution, rounding, and error statuses. Stub fetch downloads and ensure tests do not open network connections.
acceptance: yes
depends: cli_init, cli_load, cli_fetch, api_health_stats, api_currencies, api_rates, api_convert, api_history, api_reference
state: pending

## story 13: Run the supplied grader as the terminal release verification.
id: verify_release
summary: Run the supplied grader as the terminal release verification.
type: service
kind: test harness
phase: 1
block: 3
implements: VERIFICATION.md
accepts: st-001
context: run.sh
stack: common.md, python.md
stack_mode: consumer
size: 5136
instructions: Bind terminal acceptance to the supplied conformance grader over the complete application. Do not reproduce its known answers in hand-authored assertions.
acceptance: yes
depends: database, architecture, cli_init, cli_load, cli_fetch, api_health_stats, api_currencies, api_rates, api_convert, api_history, api_reference, test_suite
state: pending
