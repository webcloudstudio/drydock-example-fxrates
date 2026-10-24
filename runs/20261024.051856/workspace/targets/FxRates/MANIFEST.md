# MANIFEST: FxRates
updated: 2026-10-24T05:25:18+00:00
state: approved
blocks:      3

applied_specs: |
  ARCHITECTURE.md sha256=6f19609e3501b5c81682988bc8e666bd2505beb5942c619bd31e54613eef90f4 commit=e0bab5e343650a8177e3dfde2a2b57e5da571109 applied_by=block-2 applied_at=2026-10-24T05:31:15+00:00 build_sha256=6f19609e3501b5c81682988bc8e666bd2505beb5942c619bd31e54613eef90f4
  DATABASE.md sha256=0a49cb53f2c442a164ebfe3827cd07d7ad2d554f02ac23f0e1eaa9d3ffbe5100 commit=e0bab5e343650a8177e3dfde2a2b57e5da571109 applied_by=block-2 applied_at=2026-10-24T05:31:15+00:00 build_sha256=293b0c4c22b3519e68c36b6e220cdb1a4f920794fe25925cdd06d4c3791c67f2 database_operations=FEATURE-RATE-001:639f5f4e961f7c4712c34e4924ea8279b7c434a6f3472a232ba6a4e707a04d27;FEATURE-RATE-002:a234b2347debff12246b10c32e0d206037988ca2a4ddb522f75d025569dfcfef;FEATURE-RATE-003:8f46281079dfeb5faff8fde71239e237328f20d68fda3af92bffaac518dbea05;FEATURE-RATE-004:5de1134611ee5368a0cc1681f35ea07828a4848c4a98c87a684d9e91113a3434
  FEATURE-API-Foundation.md sha256=3bd82a94133e2567f1b28b17182e87e58abe1460968cba1cc6c04c0891dddf9e commit=e0bab5e343650a8177e3dfde2a2b57e5da571109 applied_by=block-2 applied_at=2026-10-24T05:31:15+00:00 build_sha256=b3b9f703ba479b0818185538caca0bc9e636e9cb0e8bef022b8d676dad5ac880
  FEATURE-CLI-Foundation.md sha256=0493309e99f4baf7317d65350cbe1cf4b2818d9b298e4af29a30baad26d540ff commit=e0bab5e343650a8177e3dfde2a2b57e5da571109 applied_by=block-2 applied_at=2026-10-24T05:31:15+00:00 build_sha256=ef1a4ffe3fb9c7219ed1f02e10051650d27f8355339bad7b2a6b9ae5faac9105

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
  Define the application structure, module ownership, and permitted persistence access boundary.
stack:        common.md, python.md
stack_mode:   builder
size:         3848
provides:     application module boundaries
acceptance:   yes
state: closed/implemented

## story 2: Declare the rates schema and generated persistence operations.
id:           database
finding: ADVISORY: implemented, not verified — no governed acceptance command covers this story. Declare one in ACCEPTANCE.json to gate it.
evidence: evidence/block-2.md
summary:      Declare the rates schema and generated persistence operations.
type:         foundational
kind:         capability
phase:        1
block:        2
implements:   DATABASE.md
instructions: |
  Declare the rates table and every repository operation needed by ingestion and API behavior.
  Preserve published rate text and access the database only through the generated persistence package.
stack:        persistence.md, sqlite.md
stack_mode:   builder
size:         8887
provides:     rates repository operations
depends:      architecture
acceptance:   yes
state: closed/implemented

## story 3: Establish the FastAPI application and server test client.
id: app-server-foundation
finding: ADVISORY: implemented, not verified — no governed acceptance command covers this story. Declare one in ACCEPTANCE.json to gate it.
evidence: evidence/block-2.md
summary: Establish the FastAPI application and server test client.
type: foundational
kind: capability
phase: 1
block: 2
implements: FEATURE-API-Foundation.md
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, python.md
stack_mode: builder
size: 4272
provides: app_server.main:create_app, app_server.testing:web_client
instructions: Establish the FastAPI application factory and the published in-process test client contract.
acceptance: yes
depends: architecture
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
stack: cli.md, python.md
stack_mode: builder
size: 5452
provides: ./fxrates entry point
instructions: Establish the executable entry point and command dispatch structure required by the CLI stories.
acceptance: yes
depends: architecture
state: closed/implemented

## story 5: Initialize the rates store from the CLI.
id: ingest_001
finding: step block-3 failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit-rate
evidence: evidence/block-3.md
summary: Initialize the rates store from the CLI.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Initialize-Store.md
covers: INGEST-001
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md, sqlite.md
stack_mode: consumer
size: 7259
provides: fxrates init
consumes: rates repository operations
instructions: Implement fxrates init to drop and recreate the rates table, producing no standard output.
acceptance: yes
depends: cli-foundation, database
state: closed/failed

## story 6: Validate and load ECB history files.
id: ingest_002
finding: step block-3 failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit-rate
evidence: evidence/block-3.md
summary: Validate and load ECB history files.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Load-History.md
covers: INGEST-002
accepts: st-003, st-008
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md, python.md, sqlite.md
stack_mode: consumer
size: 7744
provides: fxrates load
consumes: rates repository operations
instructions: |
  Validate the complete CSV before writing. Ignore the trailing empty field and N/A values,
  preserve each stored rate exactly as published, replace existing date and currency rates,
  and report the number of dates and rates loaded.
acceptance: yes
depends: ingest_001
state: closed/failed

## story 7: Reject invalid ECB history files atomically.
id: ingest_003
finding: step block-3 failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit-rate
evidence: evidence/block-3.md
summary: Reject invalid ECB history files atomically.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Reject-History.md
covers: INGEST-003
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md, python.md, sqlite.md
stack_mode: consumer
size: 7542
provides: atomic invalid-file rejection
consumes: fxrates load, rates repository operations
instructions: Ensure malformed rows, dates, or values reject the file with exit code 3 and leave stored data unchanged.
acceptance: yes
depends: ingest_002
state: closed/failed

## story 8: Fetch and load the ECB history archive.
id: ingest_004
finding: step block-3 failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit-rate
evidence: evidence/block-3.md
summary: Fetch and load the ECB history archive.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Fetch-History.md
covers: INGEST-004
accepts: st-009
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md, python.md, sqlite.md
stack_mode: consumer
size: 7733
provides: fxrates fetch
consumes: fxrates load
instructions: |
  Download and extract the ECB history archive, then pass the extracted CSV through the shared
  history loader. Keep the download boundary stub-able so automated tests use no network.
acceptance: yes
depends: ingest_002
state: closed/failed

## story 9: List currencies available in stored rates.
id: api_002
finding: step block-3 failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit-rate
evidence: evidence/block-3.md
summary: List currencies available in stored rates.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Currencies.md
covers: API-002
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, python.md, sqlite.md
stack_mode: consumer
size: 6006
provides: GET /currencies
consumes: rates repository operations
instructions: Return EUR as the base and currencies present in stored rates in ascending order.
acceptance: yes
depends: app-server-foundation, database
state: closed/failed

## story 10: Serve health and rate-store statistics.
id: api_001
finding: step block-3 failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit-rate
evidence: evidence/block-3.md
summary: Serve health and rate-store statistics.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Health-Stats.md
covers: API-001
accepts: st-004
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, python.md, sqlite.md
stack_mode: consumer
size: 6184
provides: GET /health, GET /stats
consumes: rates repository operations
instructions: Return the specified health response and live counts and date bounds from the rates store.
acceptance: yes
depends: app-server-foundation, database
state: closed/failed

## story 11: Return bounded currency history and summary statistics.
id: api_005
finding: programmatic acceptance failed: history-route-empty-range: AssertionError
evidence: evidence/block-3.md
summary: Return bounded currency history and summary statistics.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-History.md
covers: API-005
accepts: st-006
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, python.md, sqlite.md
stack_mode: consumer
size: 6279
provides: GET /history/{code}
consumes: rates repository operations
instructions: |
  Return inclusive date-bounded publication points and exact minimum, maximum, and half-even
  six-place mean. Return 404 when the currency has no stored history.
acceptance: yes
depends: app-server-foundation, database
state: closed/failed

## story 12: Resolve rates for requested and latest dates.
id: api_003
finding: programmatic acceptance failed: date-resolves-to-effective-publication, latest-rates-route-works: AssertionError
evidence: evidence/block-3.md
summary: Resolve rates for requested and latest dates.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Rates.md
covers: API-003
accepts: st-005
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, python.md, sqlite.md
stack_mode: consumer
size: 6326
provides: GET /rates/{date}, GET /rates/latest
consumes: rates repository operations
instructions: |
  Resolve each request to the latest publication on or before the requested date, return all rates
  for that publication, and return 404 when no earlier publication exists.
acceptance: yes
depends: app-server-foundation, database
state: closed/failed

## story 13: Convert amounts between currencies.
id: api_004
finding: programmatic acceptance failed: euro-conversion-uses-implicit-unit-rate: AssertionError
evidence: evidence/block-3.md
summary: Convert amounts between currencies.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Convert.md
covers: API-004
accepts: st-006
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, python.md, sqlite.md
stack_mode: consumer
size: 6470
provides: GET /convert
consumes: rates repository operations
instructions: |
  Compute conversions with Decimal from stored rates, rounding the rate to six places and the
  result to two places using half-even rounding.
acceptance: yes
depends: app-server-foundation, database
state: closed/failed

## story 14: Run the HTTP service on the requested localhost port.
id: cli_002
finding: step block-3 failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit-rate
evidence: evidence/block-3.md
summary: Run the HTTP service on the requested localhost port.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-Serve.md
covers: CLI-002
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md, fastapi.md, python.md
stack_mode: consumer
size: 5791
provides: fxrates serve
consumes: app_server.main:create_app
instructions: |
  Run uvicorn in the foreground bound to 127.0.0.1, using port 8000 by default or the requested
  integer port, and stop cleanly on SIGTERM.
acceptance: yes
depends: cli-foundation, app-server-foundation
state: closed/failed

## story 15: Return usage errors for invalid CLI invocations.
id: cli_001
finding: step block-3 failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit-rate
evidence: evidence/block-3.md
summary: Return usage errors for invalid CLI invocations.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-CLI-Usage.md
covers: CLI-001
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: cli.md, python.md
stack_mode: consumer
size: 5553
provides: CLI usage error behavior
consumes: ./fxrates entry point
instructions: |
  Return exit code 2 without standard output for unknown commands, wrong argument counts, and
  non-integer port values.
acceptance: yes
depends: cli-foundation
state: closed/failed

## story 16: Validate API dates, amounts, and currencies.
id: api_006
finding: step block-3 failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit-rate
evidence: evidence/block-3.md
summary: Validate API dates, amounts, and currencies.
type: service
kind: capability
phase: 1
block: 3
implements: FEATURE-API-Validation.md
covers: API-006
accepts: st-007
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: fastapi.md, python.md
stack_mode: consumer
size: 4323
provides: API request validation behavior
consumes: GET /rates/{date}, GET /convert, GET /history/{code}
instructions: |
  Ensure malformed dates and amounts and missing required query parameters return 422, while
  unknown currencies return 404.
acceptance: yes
depends: api_003, api_004, api_005
state: closed/failed

## story 17: Verify the completed application with the supplied grader.
id: verify_001
finding: step block-3 failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit-rate
evidence: evidence/block-3.md
summary: Verify the completed application with the supplied grader.
type: service
kind: test harness
phase: 1
block: 3
implements: VERIFICATION.md
covers: VERIFY-001
accepts: st-001, st-002
context: run.sh
stack: common.md, python.md, pytest
stack_mode: builder
size: 6163
instructions: |
  Run the supplied end-to-end grader as the terminal full-suite gate. Provide bin/test.sh for the
  project's pytest suite and ensure both verification commands succeed.
acceptance: yes
depends: architecture, database, cli-foundation, app-server-foundation, ingest_001, ingest_002, ingest_003, ingest_004, api_001, api_002, api_003, api_004, api_005, api_006, cli_001, cli_002
state: closed/failed
