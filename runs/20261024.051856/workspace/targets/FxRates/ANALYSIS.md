# Blueprint Analysis: FxRates

## Commander Expectations

- assert the service provides ECB euro reference rates through a command line and JSON API.
- assert conversions use exact decimal arithmetic and the specified rounding.
- assert rejected history files leave stored data unchanged.

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: History Ingestion

| ID | Story | High-level AC |
|---|---|---|
| INGEST-001 | Initialize the rates store | `fxrates init` drops and creates the rates table, with no standard output. |
| INGEST-002 | Load ECB history files | Valid rows load published rate text, skip `N/A`, replace existing rates, and report date and rate counts. |
| INGEST-003 | Reject invalid history files atomically | Invalid rows reject the file with exit code 3 and leave stored data unchanged. |
| INGEST-004 | Fetch and load ECB history | `fxrates fetch` downloads and extracts the ECB history file, then loads it using the history-file rules. |

### Feature: Rates API

| ID | Story | High-level AC |
|---|---|---|
| API-001 | Serve health and store statistics | The service returns the specified health response and rate-store counts and date bounds. |
| API-002 | List available currencies | The service returns EUR as the base and stored currencies in ascending order. |
| API-003 | Resolve rates by effective date | Date and latest requests return rates for the latest publication on or before the requested date; no earlier publication returns 404. |
| API-004 | Convert between currencies | The service returns the effective date, echoed amount, six-place half-even rate, and two-place half-even result. |
| API-005 | Read currency history | The service returns bounded publication points and exact min, max, and six-place half-even mean; a currency without stored history returns 404. |
| API-006 | Validate API requests | Malformed dates and amounts and missing required parameters return 422; unknown currencies return 404. |

### Feature: Command-Line Interface

| ID | Story | High-level AC |
|---|---|---|
| CLI-001 | Report command usage errors | Unknown commands, wrong argument counts, and invalid port values return exit code 2 without standard output. |
| CLI-002 | Run the HTTP service | `fxrates serve` binds uvicorn to 127.0.0.1 at the requested port, or port 8000 by default. |

### Feature: Verification

| ID | Story | High-level AC |
|---|---|---|
| VERIFY-001 | Pass the supplied end-to-end grader | The complete supplied grader passes against the application and its database-backed API. |

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
| `sources/INSTRUCTIONS.md` | instruction-to-test | `sources/run.sh` | The instructions define command and API behavior; the harness invokes the CLI and checks HTTP responses against known answers. | Implement the described behavior and use the staged harness for terminal acceptance. |
| `sources/run.sh` | test-kit-to-implementation | `fxrates` CLI and API | The harness invokes `./fxrates`, loads the supplied CSV files, and requests local endpoints. | Build the executable and service before running the harness. |
| `sources/eurofxref-hist_2025-01.csv`, `sources/eurofxref-hist_2025-02-03_04.csv`, `sources/eurofxref-hist_bad.csv` | fixture-to-implementation | History ingestion and API | The harness loads valid files, reloads one, and checks rejection of the malformed file. | Stage the CSV fixtures alongside the harness and cover atomic rejection and replacement. |

## Source Roles

| Path | Role | Plan disposition | Build disposition |
|---|---|---|---|
| `sources/INSTRUCTIONS.md` | normative specification and conformance test suite | prompt-only | none |
| `sources/run.sh` | conformance harness | context | stage |
| `sources/eurofxref-hist_2025-01.csv` | asset | context | stage |
| `sources/eurofxref-hist_2025-02-03_04.csv` | asset | context | stage |
| `sources/eurofxref-hist_bad.csv` | asset | context | stage |

## Planning Instructions

### Delivery Shape

Build a Python command-line application that initializes a relational rates store, loads ECB history CSV files, and serves a JSON API on localhost. The main flow is initialize the store, load history, start the server, then request health, statistics, rates, conversions, or currency history. Fetch is an alternate ingestion flow that downloads and loads the ECB history archive.

### Story Realization Map

| Story ID | Durable Blueprint scope | Evidence | Related files | Delivery implication |
|---|---|---|---|---|
| INGEST-001 | Store initialization command | `sources/INSTRUCTIONS.md` Database and Command line | `fxrates`, persistence library | Implement the reset-and-create operation using the shipped persistence boundary. |
| INGEST-002 | CSV parsing and load command | `sources/INSTRUCTIONS.md` ECB history file rules and Command line | `sources/eurofxref-hist_2025-01.csv`, `sources/eurofxref-hist_2025-02-03_04.csv` | Validate the complete input before writing; preserve published rate text and report counts. |
| INGEST-003 | Atomic rejection behavior | `sources/INSTRUCTIONS.md` ECB history file rules and Exit codes | `sources/eurofxref-hist_bad.csv` | Reject malformed input without partial writes and return the specified code. |
| INGEST-004 | Fetch command | `sources/INSTRUCTIONS.md` Command line and Tests | Stubbed download in application tests | Isolate download behavior so tests can stub it; load the extracted history through the shared loader. |
| API-001 | Health and statistics endpoints | `sources/INSTRUCTIONS.md` HTTP API | Persistent store | Provide live store statistics and health response. |
| API-002 | Currency listing endpoint | `sources/INSTRUCTIONS.md` HTTP API | Persistent store | Return currencies present in stored rates in sorted order. |
| API-003 | Effective-date rates endpoints | `sources/INSTRUCTIONS.md` HTTP API | Persistent store | Resolve publications by date, including latest and no-prior-publication behavior. |
| API-004 | Conversion endpoint | `sources/INSTRUCTIONS.md` HTTP API Values and Errors | Persistent store; Decimal arithmetic | Use exact decimal arithmetic and independently round rate and result. |
| API-005 | History endpoint | `sources/INSTRUCTIONS.md` HTTP API | Persistent store; Decimal arithmetic | Return inclusive date-bounded points and exact summary statistics. |
| API-006 | Request validation | `sources/INSTRUCTIONS.md` HTTP API Errors | Rates, conversion, and history routes | Validate dates and amounts and preserve required status behavior. |
| CLI-001 | Usage and argument errors | `sources/INSTRUCTIONS.md` Exit codes | `fxrates` | Return usage exit code for unsupported commands and malformed invocation. |
| CLI-002 | Server command | `sources/INSTRUCTIONS.md` Command line | FastAPI application, uvicorn | Bind to the specified localhost port and retain the default port. |
| VERIFY-001 | Complete supplied grader verification | `sources/run.sh` | All implementation stories and staged source fixtures | Terminal acceptance depends on all implementation stories and runs the unfiltered grader. |

### Test and Acceptance Strategy

Use focused tests for each command, parsing rule, endpoint, validation path, effective-date resolution, and rounding behavior. Stub fetch downloads in automated tests so they do not access the network. The terminal verification story runs the complete supplied `sources/run.sh` grader after implementation stories are complete. Sea Trials independently record project-wide acceptance.

### Sequencing and Dependencies

Implement the persistence boundary and store initialization before loading and API reads. Build CSV validation before writes so invalid files cannot partially change state. Implement shared date resolution before rates and conversion routes. Build API routes before the terminal grader. Fetch depends on the loader and a stub-able download boundary.

### Source Conflicts and Gaps

No unresolved source conflicts or product decisions were identified. The supplied service has no human-facing screens; the API and CLI are its entry points. The source requires persistence access through the shipped library and generated relational layer.

## Analysis Notes
generated: 2026-10-24
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.051856/workspace/targets/FxRates/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 4
  stories: 12
  stack: Python 3.11+, FastAPI, uvicorn, SQLite, pytest
  display_name: not proposed
  short_description: not proposed

Project type is mixed: the sources describe both a programmatic API and CLI commands. The terminal verification story is the sole full-suite gate.
