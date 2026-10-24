# Blueprint Analysis: FxRates

## Commander Expectations

- assert the product loads ECB euro reference rates and serves date-based rates, conversions, and currency history through a JSON API
- assert the service uses exact decimal arithmetic and retains published rates as text
- assert invalid ECB files leave stored data unchanged

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: Command Line and Data Loading

| ID | Story | High-level AC |
|---|---|---|
| CLI-001 | Initialize the rates database | `fxrates init` creates an empty rates table and prints nothing. |
| CLI-002 | Load an ECB history CSV | Valid files load non-N/A rates as published text, replace matching stored rates, and report date and rate totals; invalid files store nothing and return the specified exit code. |
| CLI-003 | Fetch and load ECB history | `fxrates fetch` downloads and extracts the ECB history file, then loads it using the CSV rules and output format. |
| CLI-004 | Start the API server | `fxrates serve` runs the service on `127.0.0.1` at the requested port or default port. |
| CLI-005 | Handle command usage and operational errors | Unknown commands, invalid arguments, unreadable files, and failed downloads return their specified exit codes; failures print no standard output and one diagnostic line to standard error. |

### Feature: Rates API

| ID | Story | High-level AC |
|---|---|---|
| API-001 | Report service health and stored-data statistics | `/health` reports `{"status":"ok"}`; `/stats` reports stored date and rate totals and the first and last dates, or null dates when empty. |
| API-002 | List available currencies | `/currencies` returns EUR as the base and stored currencies in ascending order. |
| API-003 | Resolve rates by requested or latest date | `/rates/{date}` and `/rates/latest` return rates for the latest publication on or before the requested date; requests before the first publication return 404. |
| API-004 | Convert amounts between currencies | `/convert` returns the effective date, echoed amount, exact ratio rounded to six decimals, and result rounded to two decimals using half-to-even rounding. |
| API-005 | Return currency history and statistics | `/history/{code}` returns ascending points within optional inclusive bounds and exact min, max, and mean; currencies without stored rates return 404. |
| API-006 | Validate API requests and report missing data | Malformed dates and amounts and missing required parameters return 422; unknown currencies and unavailable effective dates return 404. |

### Feature: Verification

| ID | Story | High-level AC |
|---|---|---|
| TEST-001 | Provide a network-free automated test suite | `bin/test.sh` runs the project pytest suite and exits zero only when every automated test passes; fetch tests use a stubbed download. |
| TEST-002 | Verify complete supplied-grader conformance | The terminal verification runs the supplied grader unfiltered and succeeds only when every supplied check passes. |

## Story Guidance

Named stories planning must produce. Authoritative record: `STORY_GUIDANCE.json`.

None.

## Surfaced Acceptance Criteria

None.

## Source Inventory

| Path | Content kind | Disposition | Reason |
|---|---|---|---|
| `sources/INSTRUCTIONS.md` | markdown | analyzed | readable UTF-8 |
| `sources/eurofxref-hist_2025-01.csv` | text | analyzed | readable UTF-8 |
| `sources/eurofxref-hist_2025-02-03_04.csv` | text | analyzed | readable UTF-8 |
| `sources/eurofxref-hist_bad.csv` | text | analyzed | readable UTF-8 |
| `sources/run.sh` | code | analyzed | readable UTF-8 |

## Relationship Model

| Source or group | Relationship type | Related source or group | Evidence | Delivery implication |
|---|---|---|---|---|
| `sources/INSTRUCTIONS.md` | instruction-to-test | `sources/run.sh` | The instructions define the CLI and API contract; the harness checks command output, status codes, and JSON bodies. | Implement the specified behavior and use the staged harness for final conformance. |
| `sources/run.sh` | test-kit-to-implementation | `CLI-001`–`API-006` | The harness invokes the CLI, loads the CSV fixtures, starts the server, and issues HTTP requests. | Stage the harness and every CSV it reads; implementation stories precede terminal verification. |
| `sources/eurofxref-hist_2025-01.csv` | fixture-before-verification | `CLI-002`, `API-003`–`API-005`, `TEST-002` | The harness loads this fixture and checks rates, conversions, and history. | Stage the fixture at its required `sources/` path. |
| `sources/eurofxref-hist_2025-02-03_04.csv` | fixture-before-verification | `CLI-002`, `API-001`, `API-003`, `API-005`, `TEST-002` | The harness loads it while the server is running and checks updated results. | Stage the fixture; support visibility of completed loads on subsequent requests. |
| `sources/eurofxref-hist_bad.csv` | fixture-before-verification | `CLI-002`, `TEST-002` | The harness checks rejection of a file with an invalid rate after a valid row. | Stage the fixture and verify rejection is atomic. |
| `sources/INSTRUCTIONS.md` | implementation-to-helper | `TEST-001` | The instructions require pytest, FastAPI TestClient, a temporary database, and stubbed fetch tests. | Provide the project test runner and test suite without network access. |

## Source Roles

| Path | Role | Plan disposition | Build disposition |
|---|---|---|---|
| `sources/INSTRUCTIONS.md` | normative specification and conformance test suite | prompt-only | prompt-only |
| `sources/run.sh` | conformance harness | context | stage |
| `sources/eurofxref-hist_2025-01.csv` | asset | context | stage |
| `sources/eurofxref-hist_2025-02-03_04.csv` | asset | context | stage |
| `sources/eurofxref-hist_bad.csv` | asset | context | stage |

## Planning Instructions

### Delivery Shape

This is a local CLI and JSON API service. The CLI initializes the database, loads ECB CSV history, fetches and loads the published history, and starts the server. The API reports health and database statistics, lists available currencies, resolves rates by effective publication date, converts amounts, and returns currency history. The required flow is database initialization, fixture or fetched-data loading, server startup, then API requests. A load completed while the server runs must appear on the next request.

### Story Realization Map

| Story ID | Durable Blueprint scope | Evidence | Related files | Need |
|---|---|---|---|---|
| CLI-001 | Database initialization command | `sources/INSTRUCTIONS.md` — Command line, Database | Persistence library and relational layer | capability |
| CLI-002 | CSV validation and loading command | `sources/INSTRUCTIONS.md` — ECB history file rules, Exit codes | Three staged CSV fixtures | capability, test harness |
| CLI-003 | ECB download and archive extraction command | `sources/INSTRUCTIONS.md` — Command line, fetch rules | ECB download source | integration, test harness |
| CLI-004 | Uvicorn service command and bind behavior | `sources/INSTRUCTIONS.md` — Command line, HTTP API | FastAPI application | capability |
| CLI-005 | CLI usage and operational error behavior | `sources/INSTRUCTIONS.md` — Exit codes | CLI entry point | capability, test harness |
| API-001 | Health and aggregate stats routes | `sources/INSTRUCTIONS.md` — HTTP API | Persistence repository | capability |
| API-002 | Currency listing route | `sources/INSTRUCTIONS.md` — HTTP API | Persistence repository | capability |
| API-003 | Effective-date and latest-rates routes | `sources/INSTRUCTIONS.md` — HTTP API | Persistence repository | capability |
| API-004 | Exact currency conversion route | `sources/INSTRUCTIONS.md` — HTTP API, Values | Persistence repository, Decimal arithmetic | capability |
| API-005 | Currency history route | `sources/INSTRUCTIONS.md` — HTTP API, Values | Persistence repository, Decimal arithmetic | capability |
| API-006 | Request validation and not-found responses | `sources/INSTRUCTIONS.md` — Errors | API routes | capability |
| TEST-001 | Project pytest suite and `bin/test.sh` | `sources/INSTRUCTIONS.md` — Tests | Stubbed fetch, temporary database | test harness |
| TEST-002 | Full supplied-grader verification | `sources/run.sh` | Staged harness and CSV fixtures | acceptance contract |

### Test and Acceptance Strategy

Focused pytest tests cover each command, CSV validation rule, endpoint, effective-date behavior, rounding case, and error status against a temporary database; fetch tests stub the download and open no network connection. The supplied grader is the final unfiltered verification and must pass every supplied case. TEST-002 is the sole terminal verification story and gates on the complete supplied grader; it follows all implementation stories.

### Sequencing and Dependencies

The database and persistence boundary support initialization, loading, and all routes. CSV validation must complete before writes so rejected files remain atomic. Implement CLI behavior and API capabilities before final verification. The fetch command depends on the download and archive extraction integration; its tests use a stub. Stage `sources/run.sh` and its three CSV inputs before TEST-002. `bin/test.sh` and the project tests support implementation-level verification; TEST-002 is the final full-suite gate.

### Source Conflicts and Gaps

The sources consistently specify a local FastAPI JSON service and CLI. No human-owned product decisions remain open. The source names SQLite and a shipped persistence library but does not name the library implementation; follow the generated persistence boundary and selected stack guidance.

## Analysis Notes
generated: 2026-10-24
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.224730/workspace/targets/FxRates/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 3
  stories: 14
  stack: Python 3.11+, FastAPI, uvicorn, SQLite, pytest
  display_name: not proposed
  short_description: not proposed

Project type: ambiguous (the sources describe both CLI commands and programmatic HTTP API endpoints). The API is the primary product surface; there are no human-facing screens.
