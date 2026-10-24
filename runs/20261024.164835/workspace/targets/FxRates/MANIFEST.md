# MANIFEST: FxRates
updated:     2026-10-24T16:52:19+00:00
state:       approved
blocks:      3

applied_specs: |
  ARCHITECTURE.md sha256=56a190fe12e4c91ef834fd0f9f064a75b62ed94ade400a1205ce945f80b666a9 commit=f8d9d1ca98d75f966062f0159963331f07414714 applied_by=block-1 applied_at=2026-10-24T16:57:27+00:00 build_sha256=56a190fe12e4c91ef834fd0f9f064a75b62ed94ade400a1205ce945f80b666a9
  ARCHITECTURE_compact.md sha256=4ba8bddaf651575528511269a2e02d499ca756fca914b893bbb3748283dc7267 commit=bc7e9b9d4a6b4230371702d17a2d0bf604f94ef7 applied_by=block-2 applied_at=2026-10-24T16:59:16+00:00 build_sha256=4ba8bddaf651575528511269a2e02d499ca756fca914b893bbb3748283dc7267
  DATABASE.md sha256=eb20e468d257f245e115cdae4c69932723bd538b6c0ec34c7f9ecb2288e9870c commit=f8d9d1ca98d75f966062f0159963331f07414714 applied_by=block-2 applied_at=2026-10-24T16:59:16+00:00 build_sha256=a47cce335669269a2af6254d13a7c9509eaf504c55f0fa70afa7633f09bbd805 database_operations=FEATURE-ECB-001:b5671d4f0205b138e2ce400dba5dc81566b20d685b14900e435a630d77efb5ba;FEATURE-API-001:30e597df5a35ff18b8bf80abd6333f88029662f2f7ce9cee6d9864ca4956b701;FEATURE-API-002:9516a36e60422501e900d713b75dffb3af37c066268006e25eb74596bbd278a4;FEATURE-API-003:2ae5d1edfd36ced5b47f5590c2c8ca0e2ac47cae61d24b55a68cdd8e6af8beea;FEATURE-API-004:2fbd4c56430a724f3ac3a38850c85fa09c5e1e37dec37fef08046dd3834f4f57;FEATURE-API-005:02f121e3b2cf2d67b73df72b72e0061f238d1d4ec0643890bac39309d5896d12
  FEATURE-API-Foundation.md sha256=21b2792a7f7584caff3695ac67a430f2f409e433a3ae1d4ae2d68e5886b7eb3e commit=f8d9d1ca98d75f966062f0159963331f07414714 applied_by=block-2 applied_at=2026-10-24T16:59:16+00:00 build_sha256=5255a413f03ad32f8fae2956883d28f5277865da2167d37ae021dc37a41f41be
  FEATURE-CLI-Foundation.md sha256=9b7a67efc4323896b27f17a42ceae91c6a91b007fc604df2223f77f5e68fe39c commit=f8d9d1ca98d75f966062f0159963331f07414714 applied_by=block-2 applied_at=2026-10-24T16:59:16+00:00 build_sha256=6eccf3aedd78f7e7d847dc5d539aac0d2cc3c45800e7b7a06b914dc2a0d42646
## story 1: Establish the Python application structure and boundary ownership.
id:           architecture-foundation
finding: ADVISORY: implemented, not verified — no governed acceptance command covers this story. Declare one in ACCEPTANCE.json to gate it.
evidence: evidence/block-1.md
summary:      Establish the Python application structure and boundary ownership.
type:         foundational
kind:         capability
phase:        1
block:        1
implements:   ARCHITECTURE.md
instructions: |
  Establish the Python application structure, module ownership, and configuration boundary described by ARCHITECTURE.md.

  Keep database-driver access inside the shipped persistence library. Resolve database configuration from DATABASE_URL, then DATABASE_PATH, then data/app.db.
stack:        python.md
stack_mode:   builder
size:         2538
provides:     application modules, configuration boundary
acceptance:   yes
state: closed/implemented

## story 2: Declare the rates store and generated persistence operations.
id: database-foundation
finding: ADVISORY: implemented, not verified — no governed acceptance command covers this story. Declare one in ACCEPTANCE.json to gate it.
evidence: evidence/block-2.md
summary: Declare the rates store and generated persistence operations.
type: foundational
kind: capability
phase: 1
block: 2
implements: DATABASE.md
context: INSTRUCTIONS.md
stack: persistence.md, sqlite.md
stack_mode: builder
size: 11631
provides: rates repository operations
instructions: |
  Declare the rates table and every repository operation required by loading, statistics, effective-date rates, conversions, and history.
  
  Preserve rate values as text and use the generated persistence package for all database access.
acceptance: yes
depends: architecture-foundation
state: closed/implemented

## story 3: Establish the FastAPI application and test client.
id: api-foundation
finding: ADVISORY: implemented, not verified — no governed acceptance command covers this story. Declare one in ACCEPTANCE.json to gate it.
evidence: evidence/block-2.md
summary: Establish the FastAPI application and test client.
type: foundational
kind: capability
phase: 1
block: 2
implements: FEATURE-API-Foundation.md
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md
stack_mode: builder
size: 5323
provides: app_server.main:create_app, app_server.testing:web_client
instructions: Establish the FastAPI application factory, module-level app, and published TestClient helper. Provide the shared service foundation used by the API capability stories.
acceptance: yes
depends: architecture-foundation
state: closed/implemented

## story 4: Establish the fxrates command entry point.
id: cli-foundation
finding: ADVISORY: implemented, not verified — no governed acceptance command covers this story. Declare one in ACCEPTANCE.json to gate it.
evidence: evidence/block-2.md
summary: Establish the fxrates command entry point.
type: foundational
kind: capability
phase: 1
block: 2
implements: FEATURE-CLI-Foundation.md
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md
stack_mode: builder
size: 6489
provides: ./fxrates, cli.main, cli.testing:cli_runner
instructions: Establish the executable and callable CLI entry point with the published in-process test helper. Provide the shared command foundation used by CLI capability stories.
acceptance: yes
depends: architecture-foundation
state: closed/implemented

## story 5: Initialize an empty rates store from the command line.
id: ecb-init
summary: Initialize an empty rates store from the command line.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-ECB-Init.md
covers: ECB-001
context: INSTRUCTIONS.md, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, sqlite.md, cli.md
stack_mode: consumer
size: 10547
provides: fxrates init
consumes: rates repository operations
instructions: Implement fxrates init so it drops and recreates the rates table empty, using the configured store and the persistence boundary.
acceptance: yes
depends: database-foundation, cli-foundation
state: pending

## story 6: Validate and atomically load ECB CSV history.
id: ecb-load
summary: Validate and atomically load ECB CSV history.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-ECB-Load.md
covers: ECB-002
accepts: st-003
context: INSTRUCTIONS.md, eurofxref-hist_2025-01.csv, eurofxref-hist_bad.csv, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, sqlite.md, cli.md
stack_mode: consumer
size: 11671
provides: fxrates load
consumes: rates repository operations
instructions: Implement complete-file validation before writes. Ignore the trailing empty CSV field, skip N/A values, preserve published rate text, reject invalid or repeated dates and invalid values atomically, replace matching date/currency rates, and report date and rate counts.
acceptance: yes
depends: database-foundation, cli-foundation
state: pending

## story 7: Download and load ECB history from the published ZIP.
id: ecb-fetch
summary: Download and load ECB history from the published ZIP.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-ECB-Fetch.md
covers: ECB-003
context: INSTRUCTIONS.md, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, sqlite.md, cli.md
stack_mode: consumer
size: 10641
provides: fxrates fetch
consumes: fxrates load
instructions: |
  Implement fetch by downloading the ECB history ZIP, extracting eurofxref-hist.csv, and applying the same validation, storage, and reporting rules as load.
  
  Tests must replace the download with a stub and make no network connection.
acceptance: yes
depends: ecb-load
state: pending

## story 8: Report stored publication statistics and currencies.
id: api-stats
summary: Report stored publication statistics and currencies.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-Stats.md
covers: ECB-004
context: INSTRUCTIONS.md, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, sqlite.md, fastapi.md
stack_mode: consumer
size: 9501
provides: GET /stats, GET /currencies
consumes: rates repository operations
instructions: Implement the statistics and currencies JSON endpoints. Derive counts and date bounds from stored rates; return distinct stored currencies in ascending order.
acceptance: yes
depends: database-foundation, api-foundation
state: pending

## story 9: Retrieve rates for an effective or latest publication date.
id: api-rates
summary: Retrieve rates for an effective or latest publication date.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-Rates.md
covers: API-002, API-003
accepts: st-005
context: INSTRUCTIONS.md, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, sqlite.md, fastapi.md
stack_mode: consumer
size: 9572
provides: GET /rates/{date}, GET /rates/latest
consumes: rates repository operations
instructions: Implement date-based and latest-rate endpoints. Resolve requests to the latest publication on or before the requested date, return all stored rates for that publication, and return 404 when no publication exists.
acceptance: yes
depends: database-foundation, api-foundation, ecb-load
state: pending

## story 10: Convert amounts between currencies using exact decimal arithmetic.
id: api-convert
summary: Convert amounts between currencies using exact decimal arithmetic.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-Convert.md
covers: API-004
accepts: st-005, st-006
context: INSTRUCTIONS.md, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, sqlite.md, fastapi.md
stack_mode: consumer
size: 9602
provides: GET /convert
consumes: rates repository operations
instructions: Implement conversion with the effective publication date, EUR's implicit rate, exact Decimal arithmetic, half-even rounding, and the specified six-decimal rate and two-decimal result strings. Compute the result from unrounded stored rates.
acceptance: yes
depends: database-foundation, api-foundation, ecb-load
state: pending

## story 11: Retrieve currency history and exact summary statistics.
id: api-history
summary: Retrieve currency history and exact summary statistics.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-History.md
covers: API-005
accepts: st-006
context: INSTRUCTIONS.md, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, sqlite.md, fastapi.md
stack_mode: consumer
size: 9790
provides: GET /history/{code}
consumes: rates repository operations
instructions: Implement inclusive optional date bounds, ascending points, exact Decimal extrema and half-even six-decimal mean, plus the specified empty-range response. Return 404 for a currency with no stored rate.
acceptance: yes
depends: database-foundation, api-foundation, ecb-load
state: pending

## story 12: Report service health.
id: api-health
summary: Report service health.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-Health.md
covers: API-001
accepts: st-004
context: INSTRUCTIONS.md, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, fastapi.md
stack_mode: consumer
size: 7132
provides: GET /health
instructions: Implement GET /health with the specified JSON health response.
acceptance: yes
depends: api-foundation
state: pending

## story 13: Serve the local JSON API with the command line.
id: cli-serve
summary: Serve the local JSON API with the command line.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-CLI-Serve.md
covers: CLI-001
accepts: st-004
context: INSTRUCTIONS.md, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, fastapi.md, cli.md
stack_mode: consumer
size: 9186
provides: fxrates serve
consumes: app_server.main:app
instructions: Implement foreground serving on 127.0.0.1 with the requested port or default 8000. Ensure the process stops cleanly on SIGTERM.
acceptance: yes
depends: api-foundation, cli-foundation, api-health
state: pending

## story 14: Report CLI usage and operational failures.
id: cli-errors
summary: Report CLI usage and operational failures.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-CLI-Errors.md
covers: CLI-002
context: INSTRUCTIONS.md, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, cli.md
stack_mode: consumer
size: 8705
provides: CLI exit codes and diagnostics
consumes: fxrates init, fxrates load, fxrates fetch, fxrates serve
instructions: Implement the specified exit codes for success, operational failures, usage errors, and rejected files. A failing command writes no stdout and one diagnostic line to stderr.
acceptance: yes
depends: cli-foundation, ecb-init, ecb-load, ecb-fetch, cli-serve
state: pending

## story 15: Return the specified errors for invalid API requests.
id: api-validation
summary: Return the specified errors for invalid API requests.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-Validation.md
covers: API-006
accepts: st-007
context: INSTRUCTIONS.md, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, fastapi.md
stack_mode: consumer
size: 7595
provides: API request validation behavior
consumes: GET /rates/{date}, GET /convert, GET /history/{code}
instructions: Ensure malformed dates and amounts and missing required query parameters return 422. Ensure unknown or unavailable currencies return 404 on the applicable routes.
acceptance: yes
depends: api-foundation, api-rates, api-convert, api-history
state: pending

## story 16: Provide the project pytest suite and POSIX test runner.
id: verification-suite
summary: Provide the project pytest suite and POSIX test runner.
type: service
kind: test harness
phase: 1
block: 3
implements: FEATURE-Verification-Suite.md
covers: VERIFY-001
accepts: st-002, st-009
context: INSTRUCTIONS.md, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md
stack_mode: consumer
size: 6868
provides: bin/test.sh, pytest suite
instructions: Provide a POSIX-compatible bin/test.sh and a pytest suite covering the commands, loading rules, endpoints, effective-date behavior, rounding, and error statuses against a real temporary database. Stub fetch downloads so tests never use the network.
acceptance: yes
depends: architecture-foundation, database-foundation, api-foundation, cli-foundation, ecb-init, ecb-load, ecb-fetch, api-stats, api-health, api-rates, api-convert, api-history, api-validation, cli-serve, cli-errors
state: pending

## story 17: Pass the supplied end-to-end grader.
id: release-verification
summary: Pass the supplied end-to-end grader.
type: service
kind: test harness
phase: 1
block: 3
implements: FEATURE-Release-Verification.md
covers: VERIFY-002
accepts: st-001
context: run.sh, eurofxref-hist_2025-01.csv, eurofxref-hist_2025-02-03_04.csv, eurofxref-hist_bad.csv, ARCHITECTURE_compact.md, DATABASE_compact.md
stack: python.md, common.md
stack_mode: builder
size: 9506
provides: full supplied grader acceptance
instructions: As the terminal story, run the complete supplied grader using its documented invocation and require exit status zero. Do not modify or substitute any staged source asset.
acceptance: yes
depends: architecture-foundation, database-foundation, api-foundation, cli-foundation, ecb-init, ecb-load, ecb-fetch, api-stats, api-health, api-rates, api-convert, api-history, api-validation, cli-serve, cli-errors, verification-suite
state: pending
