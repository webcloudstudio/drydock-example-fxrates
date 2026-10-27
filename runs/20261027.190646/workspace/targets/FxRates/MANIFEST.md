# MANIFEST: FxRates
updated:     2026-10-27T19:17:57+00:00
state:       approved
blocks:      14

applied_specs: |
  ARCHITECTURE.md sha256=89e00be8e977894123614efc8507ad660a4675307e5e2e0658a8af65bdfb37dc commit=7db01b5852fa95fb207d25f15a5c52f4e6b0074e applied_by=block-1 applied_at=2026-10-27T19:27:03+00:00 build_sha256=b59278ce2b01cede7e174f9d4419d1feff572b2c30557238e549f8d7a9fe3205
  ARCHITECTURE_compact.md sha256=aacd26c7d86581ab71afcb99b3a361e1f332330d357aa39ec5918278549644e2 commit=df9e4d275c797a11f6bd07f863634b27bb293485 applied_by=block-3 applied_at=2026-10-27T19:32:07+00:00 build_sha256=aacd26c7d86581ab71afcb99b3a361e1f332330d357aa39ec5918278549644e2
  DATABASE.md sha256=67b7e9b8bdd2c825a3fedda981b4063c04c50608d7bcf8a3f3a11f5477dd137c commit=7db01b5852fa95fb207d25f15a5c52f4e6b0074e applied_by=block-3 applied_at=2026-10-27T19:32:07+00:00 build_sha256=f149cdc22a4f8614b03934480b8a3167fb0cba0cbcceb1d16eec985904dcdeab database_operations=FEATURE-RATE-001:0a28b90bf540d0f37d171ba8f5a7e89c9478996f1b4d7f7a37e0bc721408912b;FEATURE-RATE-002:49df202966f052a405941b0b98d5ba91d2bd87729ec7e4f74f28bb68072e0362;FEATURE-RATE-003:2205db184a3205245a943c7171bb6273fcf59ccac99305264942f6b0121754bd;FEATURE-RATE-004:cd291bb32a815a9c46af5f1ad796817bbe4ef10a4b91cbd33de79de31308b7e3
  FEATURE-CliFoundation.md sha256=5fee0f6c1d367b828dcac73ff227a8823dea39b97fb7acf1322b7f8e26cd25df commit=7db01b5852fa95fb207d25f15a5c52f4e6b0074e applied_by=block-3 applied_at=2026-10-27T19:32:07+00:00 build_sha256=f3ec9021b56dcee5fbfa3d81951df00c8210981f38a55512a043c33b080f8d6b
  FEATURE-WebFoundation.md sha256=344d5bcf5b6fc65f1a459e2603ef8870b2f5d21a8eb41e78ae0a47d34e508e70 commit=7db01b5852fa95fb207d25f15a5c52f4e6b0074e applied_by=block-3 applied_at=2026-10-27T19:32:07+00:00 build_sha256=a8ba471c0b94daf0600c71379f5e416a5dc00909d3d69ebf49bf2afac50fe1b5

## story 1: Stand up the Python project root, environment, config resolution and test runner.
id:           foundation-python
finding: ADVISORY: implemented, not verified — no governed acceptance command covers this story. Declare one in ACCEPTANCE.json to gate it.
evidence: evidence/block-1.md
summary:      Stand up the Python project root, environment, config resolution and test runner.
type:         foundational
kind:         capability
phase:        1
block:        1
implements:   ARCHITECTURE.md
instructions: |
  Create the project root: pyproject.toml (Python 3.11+, fastapi, uvicorn, pytest, httpx2) and a committed
  uv.lock, a .venv created by uv venv, launchers in bin/ that activate it, and bin/test.sh, a POSIX sh
  script that runs pytest -q from the application root and exits nonzero on any failure.

  Add a config module with database_path() resolving DATABASE_URL (optional sqlite:// prefix), then
  DATABASE_PATH, then data/app.db. ARCHITECTURE.md records module ownership: persistence only through the
  shipped persistence package, no driver imports in application code, rates as text, decimal for arithmetic,
  diagnostics on stderr. Tests never touch the network.
stack:        common.md, python.md
stack_mode:   builder
size:         7736
provides:     config.database_path, bin/test.sh
acceptance:   yes
state: closed/implemented

## story 2: Declare the rates store and its repository operations; Drydock generates the persistence package.
id:           database
finding: ADVISORY: implemented, not verified — no governed acceptance command covers this story. Declare one in ACCEPTANCE.json to gate it.
evidence: evidence/block-2.md
summary:      Declare the rates store and its repository operations; Drydock generates the persistence package.
type:         foundational
kind:         capability
phase:        1
block:        2
implements:   DATABASE.md
instructions: |
  Write no persistence code; Drydock generates the package from DATABASE.md. The one table is rates
  (date TEXT, currency TEXT, rate TEXT, PK id, UNIQUE (date, currency)).

  Operations, all owned by DATABASE.md: rates.replace_rate (upsert on date, currency), rates.list_through
  (optional bound date <= through_date, order date desc, currency asc), rates.list_all (order date asc,
  currency asc), rates.history (currency, optional date >= start_date, optional date <= end_date, order
  date asc, output date and rate). Use a distinct Output DTO name per projection.
stack:        common.md, python.md, persistence.md, sqlite.md
stack_mode:   builder
size:         18881
provides:     db.rates.replace_rate, db.rates.list_through, db.rates.list_all, db.rates.history
depends:      foundation-python
acceptance:   yes
state: closed/implemented

## story 3: Provide the cli package, dispatcher, exit-code mapping and the fxrates executable.
id: foundation-cli
finding: ADVISORY: implemented, not verified — no governed acceptance command covers this story. Declare one in ACCEPTANCE.json to gate it.
evidence: evidence/block-3.md
summary: Provide the cli package, dispatcher, exit-code mapping and the fxrates executable.
type: foundational
kind: capability
phase: 1
block: 3
implements: FEATURE-CliFoundation.md
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, cli.md
stack_mode: builder
size: 15146
provides: cli.main, cli.testing.cli_runner, fxrates
consumes: config.database_path
instructions: |
  Implement cli.main(argv) -> int and cli/testing.py cli_runner per the foundation contract, plus the
  executable fxrates at the application root that activates .venv and calls cli.main.
  
  The dispatcher resolves a command by importing cli.commands.<name> and calling run(args) -> int, so
  command stories add modules without editing shared files. Define the error classes OperationalError (exit 1),
  UsageError (exit 2) and RejectedFile (exit 3); the dispatcher prints one diagnostic line to stderr, nothing
  to stdout, and returns the mapped code.
acceptance: yes
depends: foundation-python, database
state: closed/implemented

## story 4: Provide the app_server package with create_app and the web_client fixture.
id: foundation-web
finding: ADVISORY: implemented, not verified — no governed acceptance command covers this story. Declare one in ACCEPTANCE.json to gate it.
evidence: evidence/block-3.md
summary: Provide the app_server package with create_app and the web_client fixture.
type: foundational
kind: capability
phase: 1
block: 3
implements: FEATURE-WebFoundation.md
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md
stack_mode: builder
size: 13430
provides: app_server.main.create_app, app_server.testing.web_client
consumes: config.database_path
instructions: |
  Implement app_server/main.py with create_app() -> FastAPI and a module-level app, and
  app_server/testing.py web_client(). Routers are included from app_server/routers modules. A request-scoped
  dependency opens the database through persistence.open_database on each request, so loads completed by
  another process are visible to the next request. Application startup never initializes the schema.
acceptance: yes
depends: foundation-python, database
state: closed/implemented

## story 5: Implement fxrates init via persistence.initialize_database.
id: cli-init
finding: managed-state violation
evidence: evidence/block-4.md
summary: Implement fxrates init via persistence.initialize_database.
type: service
kind: capability
phase: 1
block: 4
implements: FEATURE-Init.md
covers: CLI-001
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, cli.md
stack_mode: consumer
size: 13856
provides: fxrates init
consumes: cli.main, config.database_path
instructions: |
  cli/commands/init.py calls persistence.initialize_database(dsn) with the configured location and closes
  the returned database. It prints nothing to stdout and returns 0. Repeating init succeeds and preserves
  stored rates. It never drops tables or deletes rows, and no DDL is written in application code.
acceptance: yes
depends: foundation-cli, database
state: closed/failed

## story 6: Report command usage errors with exit 2.
id: cli-usage
finding: managed-state violation
evidence: evidence/block-4.md
summary: Report command usage errors with exit 2.
type: service
kind: capability
phase: 1
block: 4
implements: FEATURE-UsageErrors.md
covers: CLI-002
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, cli.md
stack_mode: consumer
size: 13658
provides: fxrates usage validation
consumes: cli.main
instructions: |
  In the dispatcher, validate before any handler runs: no command, an unknown command, the wrong argument
  count (load takes exactly one path, init and fetch take none), and a serve --port value that is not an
  integer all exit 2 with one stderr line and empty stdout. Valid arguments reach the handler as parsed
  values (serve port defaults to 8000).
acceptance: yes
depends: foundation-cli
state: closed/failed

## story 7: Store parsed rates, replacing any existing (date, currency) rate.
id: rate-store
finding: managed-state violation
evidence: evidence/block-4.md
summary: Store parsed rates, replacing any existing (date, currency) rate.
type: service
kind: capability
phase: 1
block: 4
implements: FEATURE-RateStorage.md
covers: LOAD-003
accepts: st-003
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 11356
provides: ratestore.store_rates
consumes: db.rates.replace_rate
instructions: |
  store_rates(db, records) writes each record through db.rates.replace_rate and returns the number of
  distinct dates and of rates written. Reloading the same records leaves the database unchanged, and a
  changed rate replaces the stored one. Empty input writes nothing.
acceptance: yes
depends: database, foundation-python
state: closed/failed

## story 8: Parse and validate an ECB history CSV without writing anything.
id: load-parse
finding: managed-state violation
evidence: evidence/block-4.md
summary: Parse and validate an ECB history CSV without writing anything.
type: service
kind: capability
phase: 1
block: 4
implements: FEATURE-EcbParse.md
covers: LOAD-001
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 12283
provides: ecb.parse_history
instructions: |
  Implement ecb.parse_history(text) returning records (date, currency, rate text) for every non-N/A value.
  Header: first field Date, the rest three-letter uppercase codes, and one trailing empty field is ignored.
  Each row has the header's field count, a real unique YYYY-MM-DD date, and each value either N/A or
  matching [0-9]+(\.[0-9]+)? and nonzero. Any violation raises RejectedFile before any record is returned.
  Rate text is kept exactly as published; never convert to float.
acceptance: yes
depends: foundation-cli
state: closed/failed

## story 9: Implement fxrates load, validating the whole file before the first write.
id: load-atomic
summary: Implement fxrates load, validating the whole file before the first write.
type: service
kind: capability
phase: 1
block: 5
implements: FEATURE-LoadAtomic.md
covers: LOAD-002
accepts: st-003
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, cli.md
stack_mode: consumer
size: 15118
provides: fxrates load
consumes: ecb.parse_history, ratestore.store_rates, cli.main, fxrates init
instructions: |
  cli/commands/load.py reads the file (unreadable raises OperationalError, exit 1), calls ecb.parse_history
  on the full text (invalid raises RejectedFile, exit 3, nothing stored), then stores through
  ratestore.store_rates. Return the stored counts to the caller; stdout summary is owned by load-summary.
  A rejected file leaves the database exactly as it was.
acceptance: yes
depends: foundation-cli, cli-init, load-parse, rate-store
state: pending

## story 10: Print the dates,rates summary after a load.
id: load-summary
summary: Print the dates,rates summary after a load.
type: service
kind: capability
phase: 1
block: 6
implements: FEATURE-LoadSummary.md
covers: LOAD-004
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, cli.md
stack_mode: consumer
size: 14160
provides: fxrates load summary output
consumes: fxrates load
instructions: |
  On success print exactly the line dates,rates then a line of the two counts separated by a comma: dates
  with at least one stored rate in the file, and rates stored from the file. A date whose values are all
  N/A is not counted. Failures print nothing to stdout.
acceptance: yes
depends: load-atomic
state: pending

## story 11: Implement fxrates fetch against the ECB zip, testable with a stubbed download.
id: fetch
summary: Implement fxrates fetch against the ECB zip, testable with a stubbed download.
type: service
kind: capability
phase: 1
block: 7
implements: FEATURE-Fetch.md
covers: LOAD-005
accepts: st-010
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, cli.md
stack_mode: consumer
size: 14931
provides: fxrates fetch
consumes: fxrates load summary output, ecb.parse_history
instructions: |
  Put the download in one function, ecb.download_history(), that GETs
  https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip, extracts eurofxref-hist.csv and returns its
  text; any download or extraction failure raises OperationalError (exit 1). The command then loads and
  prints as load does. Tests replace ecb.download_history with a stub and cover a successful load and a
  failure exiting 1; no test opens a network connection.
acceptance: yes
depends: load-summary
state: pending

## story 12: Assemble and prove operational-failure handling across load and fetch.
id: cli-failures
summary: Assemble and prove operational-failure handling across load and fetch.
type: feature
kind: integration
phase: 1
block: 8
implements: FEATURE-OperationalFailures.md
covers: CLI-003
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, cli.md
stack_mode: consumer
size: 14030
provides: fxrates exit code 1 diagnostics
consumes: fxrates load, fxrates fetch
instructions: |
  Assembly and intent: an unreadable load file and a failed fetch download each exit 1, write nothing to
  stdout and one diagnostic line to stderr, and leave the database unchanged. Fix any seam that breaks this.
acceptance: yes
depends: load-atomic, fetch
state: pending

## story 13: Serve GET /health.
id: health
summary: Serve GET /health.
type: service
kind: capability
phase: 2
block: 9
implements: FEATURE-Health.md
covers: SVC-002
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md
stack_mode: consumer
size: 11670
provides: GET /health
consumes: app_server.main.create_app
instructions: Add the health router returning 200 with {"status": "ok"}. It does not touch the database.
acceptance: yes
depends: foundation-web
state: pending

## story 14: Serve GET /currencies.
id: currencies
summary: Serve GET /currencies.
type: service
kind: capability
phase: 2
block: 9
implements: FEATURE-Currencies.md
covers: STAT-002
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md
stack_mode: consumer
size: 12204
provides: GET /currencies
consumes: db.rates.list_all
instructions: |
  Return {"base": "EUR", "currencies": [...]} with every currency having at least one stored rate,
  distinct and ascending.
acceptance: yes
depends: foundation-web, database
state: pending

## story 15: Serve GET /stats.
id: stats
summary: Serve GET /stats.
type: service
kind: capability
phase: 2
block: 9
implements: FEATURE-Stats.md
covers: STAT-001
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md
stack_mode: consumer
size: 12495
provides: GET /stats
consumes: db.rates.list_all
instructions: |
  Return dates (distinct dates with a stored rate), rates (row count), first and last (min and max date,
  null when empty), computed in the service from db.rates.list_all. Acceptance seeds through db_session and
  compares counts read before and after setup rather than absolute counts.
acceptance: yes
depends: foundation-web, database
state: pending

## story 16: Serve GET /history/{code} with exact statistics.
id: history
summary: Serve GET /history/{code} with exact statistics.
type: service
kind: capability
phase: 2
block: 9
implements: FEATURE-History.md
covers: HIST-001
accepts: st-006
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md
stack_mode: consumer
size: 13596
provides: GET /history/{code}
consumes: db.rates.history
instructions: |
  Return currency, base EUR, count, min and max (stored text of the smallest and largest by decimal value),
  mean (exact decimal mean rounded half-even to six decimals, six decimals written) and points ascending by
  date, with optional inclusive start and end.
acceptance: yes
depends: foundation-web, database
state: pending

## story 17: Resolve the effective publication date and its rates.
id: effective-date
summary: Resolve the effective publication date and its rates.
type: service
kind: capability
phase: 2
block: 9
implements: FEATURE-EffectiveDate.md
covers: RATE-001
accepts: st-005
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md
stack_mode: consumer
size: 11527
provides: rates.effective_publication
consumes: db.rates.list_through
instructions: |
  Implement a service function taking a requested date or None (latest) and returning the effective date
  and that date's rates, using one db.rates.list_through call: the first row's date is the effective date
  and rows with that date are its rates. Return None when no publication is on or before the date.
  Compare dates as ISO strings. Rate values stay stored text.
acceptance: yes
depends: database, foundation-python
state: pending

## story 18: Implement fxrates serve on 127.0.0.1 with uvicorn.
id: serve
summary: Implement fxrates serve on 127.0.0.1 with uvicorn.
type: service
kind: capability
phase: 2
block: 10
implements: FEATURE-Serve.md
covers: SVC-001
accepts: st-004
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md, cli.md
stack_mode: consumer
size: 15462
provides: fxrates serve
consumes: GET /health, fxrates usage validation, cli.main
instructions: |
  cli/commands/serve.py runs uvicorn on app_server.main:app bound only to 127.0.0.1 at the given port
  (default 8000), in the foreground, and stops cleanly with exit 0 on SIGTERM. Nothing is required on
  stdout. Acceptance starts the server on a free port, waits within a deadline for GET /health, and always
  terminates and reaps the child.
acceptance: yes
depends: foundation-cli, cli-usage, health
state: pending

## story 19: Return an empty history for a known currency with no points in range.
id: history-empty
summary: Return an empty history for a known currency with no points in range.
type: service
kind: capability
phase: 2
block: 10
implements: FEATURE-HistoryEmpty.md
covers: HIST-002
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md
stack_mode: consumer
size: 12442
provides: GET /history/{code} empty
consumes: GET /history/{code}
instructions: When the range holds no points, return count 0, min, max and mean null, and points [].
acceptance: yes
depends: history
state: pending

## story 20: Serve GET /rates/{date}.
id: rates-by-date
summary: Serve GET /rates/{date}.
type: service
kind: capability
phase: 2
block: 10
implements: FEATURE-RatesByDate.md
covers: RATE-002
accepts: st-005, st-007
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md
stack_mode: consumer
size: 12678
provides: GET /rates/{date}
consumes: rates.effective_publication
instructions: |
  Parse the path date as a calendar date (malformed gives 422). Respond with date (effective), requested,
  base EUR and rates as stored-text JSON strings; 404 when no publication on or before the date.
acceptance: yes
depends: foundation-web, effective-date
state: pending

## story 21: Serve GET /convert for an explicit date with exact decimal arithmetic.
id: convert
summary: Serve GET /convert for an explicit date with exact decimal arithmetic.
type: service
kind: capability
phase: 2
block: 10
implements: FEATURE-Convert.md
covers: CONV-001
accepts: st-006
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md
stack_mode: consumer
size: 14021
provides: GET /convert
consumes: rates.effective_publication
instructions: |
  Query parameters from, to, amount, date. EUR has implicit rate 1. rate = rate(to)/rate(from) computed
  with decimal, rounded half-even to six decimals and formatted with six decimals. result =
  amount*rate(to)/rate(from) computed from the stored rates, never the rounded rate, rounded half-even to
  two decimals. amount is echoed exactly as given. All values are JSON strings.
acceptance: yes
depends: foundation-web, effective-date
state: pending

## story 22: Serve GET /rates/latest.
id: rates-latest
summary: Serve GET /rates/latest.
type: service
kind: capability
phase: 2
block: 11
implements: FEATURE-RatesLatest.md
covers: RATE-003
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md
stack_mode: consumer
size: 12184
provides: GET /rates/latest
consumes: rates.effective_publication
instructions: |
  Register this route ahead of the dated route in the same router so latest is not parsed as a date.
  Response matches /rates/{date} for the latest publication with requested set to "latest"; 404 when the
  store is empty.
acceptance: yes
depends: rates-by-date
state: pending

## story 23: Reject history requests for unknown currencies and malformed dates.
id: history-rejects
summary: Reject history requests for unknown currencies and malformed dates.
type: service
kind: capability
phase: 2
block: 11
implements: FEATURE-HistoryRejects.md
covers: HIST-003
accepts: st-007
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md
stack_mode: consumer
size: 12414
provides: GET /history/{code} rejects
consumes: GET /history/{code} empty
instructions: |
  404 when the currency has no stored rate at all, including EUR, regardless of range. 422 for a malformed
  start or end date.
acceptance: yes
depends: history-empty
state: pending

## story 24: Default /convert to the latest publication when date is omitted.
id: convert-latest
summary: Default /convert to the latest publication when date is omitted.
type: service
kind: capability
phase: 2
block: 11
implements: FEATURE-ConvertLatest.md
covers: CONV-002
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md
stack_mode: consumer
size: 12452
provides: GET /convert latest default
consumes: GET /convert, rates.effective_publication
instructions: Make date optional on /convert; when absent resolve the latest publication and return that date.
acceptance: yes
depends: convert
state: pending

## story 25: Handle /convert error statuses.
id: convert-errors
summary: Handle /convert error statuses.
type: service
kind: capability
phase: 2
block: 12
implements: FEATURE-ConvertErrors.md
covers: CONV-003
accepts: st-005, st-007
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md
stack_mode: consumer
size: 13119
provides: GET /convert errors
consumes: GET /convert latest default
instructions: |
  404 when no publication is on or before the date, or a currency other than EUR has no rate on the
  effective date. 422 for a malformed amount (must match [0-9]+(\.[0-9]+)?), malformed date or a missing
  required parameter; use FastAPI request validation.
acceptance: yes
depends: convert-latest
state: pending

## story 26: Prove a load completed while the server runs is visible to the next request.
id: live-visibility
summary: Prove a load completed while the server runs is visible to the next request.
type: feature
kind: integration
phase: 2
block: 13
implements: FEATURE-LiveVisibility.md
covers: SVC-003
context: ARCHITECTURE_compact.md, DATABASE_compact.md
stack: common.md, python.md, fastapi.md
stack_mode: consumer
size: 13141
provides: live load visibility
consumes: GET /stats, fxrates load, fxrates serve
instructions: |
  Assembly and intent: because each request opens its own database handle, a load committed after the app
  was created is reflected by the next /stats and /rates/latest request. Acceptance runs in-process: create
  the web client, read /stats, load a file through cli_runner, read /stats again.
acceptance: yes
depends: serve, stats, load-summary
state: pending

## story 27: Terminal gate running the supplied grader and the project test suite.
id:           verification
summary:      Terminal gate running the supplied grader and the project test suite.
type:         feature
kind:         integration
phase:        3
block:        14
implements:   VERIFICATION.md
accepts:      st-001, st-002, st-008, st-009
instructions: |
  Assembly and intent: run sh bin/test.sh (exit 0) and, declared Suite: full, sh sources/run.sh (exit 0),
  printing captured output before asserting. Do not edit anything under sources/. Confirm the application
  reaches the database only through the persistence package and that bin/test.sh passes with network
  access denied.
stack:        common.md, python.md
stack_mode:   consumer
size:         5658
provides:     release verification
consumes:     fxrates init, fxrates load, fxrates serve, fxrates fetch
depends:      cli-init, cli-usage, cli-failures, load-atomic, load-summary, fetch, serve, health, stats, currencies, rates-by-date, rates-latest, convert-errors, history-rejects, live-visibility
acceptance:   yes
state:        pending
