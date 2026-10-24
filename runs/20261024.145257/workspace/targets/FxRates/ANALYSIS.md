# Blueprint Analysis: FxRates

## Commander Expectations

- assert the product loads ECB euro reference rates and serves date-based rates, conversions, and currency history through a JSON API
- assert rates retain their published text and calculations use exact decimal arithmetic

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: Command-line Operations

| ID | Story | High-level AC |
|---|---|---|
| CLI-001 | Initialize the rates database | `init` creates an empty rates table and prints nothing. |
| CLI-002 | Load ECB history files | Valid files load atomically, preserve published rate text, replace matching rates, and report date and rate counts; invalid files are rejected with the specified exit codes and no partial writes. |
| CLI-003 | Fetch ECB history | `fetch` downloads and extracts the ECB history file, then loads it using the same rules as `load`; download failures return the operational failure code. |
| CLI-004 | Serve the API | `serve` starts the API on the specified port or port 8000, bound to 127.0.0.1. |

### Feature: Rates API

| ID | Story | High-level AC |
|---|---|---|
| API-001 | Report service health and rate coverage | `/health`, `/stats`, and `/currencies` return the specified JSON, including empty-database values. |
| API-002 | Retrieve rates by effective date | `/rates/{date}` and `/rates/latest` return published rates for the latest date on or before the request, or 404 when none exists; malformed dates return 422. |
| API-003 | Convert between currencies | `/convert` returns the effective date, exact six-place rate and two-place result, with half-even rounding; malformed or missing inputs return 422 and unavailable currencies or dates return 404. |
| API-004 | Retrieve currency history | `/history/{code}` returns ordered points and exact statistics within optional inclusive bounds; empty ranges return null statistics and an empty point list, malformed bounds return 422, and currencies without stored rates return 404. |

### Feature: Verification

| ID | Story | High-level AC |
|---|---|---|
| QA-001 | Verify supplied grader conformance | Running the supplied grader from the application root exits zero. |
| QA-002 | Run the automated test suite | The POSIX-compatible `bin/test.sh` exits zero when every automated test passes. |

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
| `sources/INSTRUCTIONS.md` | instruction-to-test | `sources/run.sh` | The instructions define the CLI and HTTP behavior; the harness exercises command output, statuses, and JSON bodies. | CLI and API stories implement the harness contract; QA-001 runs the staged harness. |
| `sources/run.sh` | test-kit-to-implementation | CLI and API stories | The harness initializes, loads, starts the server, and checks behavior, including a load while serving. | Implement command and API flows before QA-001; database changes must be visible to subsequent requests. |
| ECB CSV files | dependency | CLI-002 | Valid, malformed, and overlapping date/rate rows demonstrate load behavior. | Stage the supplied data files with the harness. |
| CLI-002 | dependency | API-001–API-004 | API responses are backed by rates loaded into the database. | Implement persistence and load behavior before data-backed API behavior. |
| `sources/INSTRUCTIONS.md` | dependency | QA-002 | The instructions require an automated pytest suite and POSIX runner. | Provide the runner and tests as product deliverables; no separate imported test suite is supplied. |

## Source Roles

| Path | Role | Plan disposition | Build disposition |
|---|---|---|---|
| `sources/INSTRUCTIONS.md` | normative specification and conformance test suite | prompt-only | none |
| `sources/eurofxref-hist_2025-01.csv` | asset | context | stage |
| `sources/eurofxref-hist_2025-02-03_04.csv` | asset | context | stage |
| `sources/eurofxref-hist_bad.csv` | asset | context | stage |
| `sources/run.sh` | conformance harness | context | stage |

## Planning Instructions

### Delivery Shape

A local command-line application initializes and loads ECB CSV history into SQLite, then runs a JSON API bound to localhost. The flow is initialize, load one or more files, serve, and query health, coverage, effective-date rates, conversions, or history. Fetch is an alternate ingestion flow that downloads the ECB archive and loads its history. The supplied harness exercises command behavior and API responses against a temporary database.

### Story Realization Map

| Story ID | Durable Blueprint scope | Evidence | Related files | Requires |
|---|---|---|---|---|
| CLI-001 | Database initialization command | `sources/INSTRUCTIONS.md` — Command line, Database | `fxrates` | capability |
| CLI-002 | Atomic ECB CSV loading | `sources/INSTRUCTIONS.md` — ECB history file rules, Exit codes | ECB CSV assets; `fxrates` | capability, persistence |
| CLI-003 | ECB archive fetch command | `sources/INSTRUCTIONS.md` — Command line, Tests | `fxrates` | capability, integration, test harness |
| CLI-004 | Local API server command | `sources/INSTRUCTIONS.md` — Command line, HTTP API | `fxrates` | capability |
| API-001 | Health, stats, and currencies endpoints | `sources/INSTRUCTIONS.md` — HTTP API | `fxrates` | capability, persistence |
| API-002 | Effective-date rates endpoints | `sources/INSTRUCTIONS.md` — HTTP API, Effective date | `fxrates` | capability, persistence |
| API-003 | Currency conversion endpoint | `sources/INSTRUCTIONS.md` — HTTP API, Values, Errors | `fxrates` | capability, persistence |
| API-004 | Currency history endpoint | `sources/INSTRUCTIONS.md` — HTTP API, Values, Errors | `fxrates` | capability, persistence |
| QA-001 | Supplied grader execution | `sources/INSTRUCTIONS.md` — Run Harness | `sources/run.sh`, CSV assets | acceptance contract |
| QA-002 | Automated test runner and suite | `sources/INSTRUCTIONS.md` — Tests | `bin/test.sh` and project tests | test harness |

For each persistent-data route or service, Plan should define a stable repository-call contract in `DATABASE.md`, with DTO inputs and outputs and `data` consumer sensitivity. The rates lookup, effective-date resolution, currency listing, statistics, conversion inputs, and history query are separate repository capabilities as their contracts require.

### Test and Acceptance Strategy

Use focused tests for each command and endpoint, including malformed input, rejected files, effective-date fallback, decimal rounding, empty results, and live-server visibility after a load. Stub fetch downloads so tests do not use the network. QA-001 is the final supplied-grader proof; QA-002 runs the project’s automated suite. The supplied grader and project test suite are distinct verification assets.

### Sequencing and Dependencies

Define the persistence contract and database configuration before CLI/API specifications that consume stored rates. Implement initialization and atomic loading before data-backed endpoints. Implement API routes before serving and endpoint verification. Fetch depends on the same load behavior as CLI-002. QA stories follow implementation; stage the harness and its CSV inputs for acceptance.

### Source Conflicts and Gaps

No conflicting product definitions were found. The source names Python 3.11+, FastAPI, uvicorn, SQLite, pytest, and POSIX shell. It specifies localhost operation and a stubbed fetch test, but does not prescribe a deployment target beyond the local server workflow.

## Analysis Notes
generated: 2026-10-24
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.145257/workspace/targets/FxRates/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 3
  stories: 10
  stack: Python 3.11+, FastAPI, uvicorn, SQLite, pytest, POSIX shell
  display_name: not proposed
  short_description: not proposed

Project type is ambiguous because the source describes both CLI commands and programmatic HTTP endpoints. No human-owned decisions remain open.
