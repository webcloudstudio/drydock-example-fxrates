# Blueprint Analysis: FxRates

## Commander Expectations

- assert the product provides a command-line loader and JSON API for ECB euro reference exchange rates
- assert callers can retrieve rates by effective date, convert currencies, and inspect currency history

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: Command-Line Operations

| ID | Story | High-level AC |
|---|---|---|
| CLI-001 | Initialize the rates database | `fxrates init` creates an empty rates table and prints nothing. |
| CLI-002 | Load an ECB history file | Valid CSV loads atomically, preserves published rate text, replaces matching rates, and reports date and rate counts. |
| CLI-003 | Fetch and load ECB history | `fxrates fetch` downloads and loads the ECB history archive; download failure exits 1. |
| CLI-004 | Start the HTTP service | `fxrates serve` starts the service on 127.0.0.1 at the requested port, defaulting to 8000. |
| CLI-005 | Report command usage errors | Unknown commands, incorrect argument counts, and a non-integer port exit 2 without standard output. |

### Feature: Rates API

| ID | Story | High-level AC |
|---|---|---|
| API-001 | Report service health and database statistics | Health returns `{"status":"ok"}`; stats reports date and rate counts and first and last dates, or null dates when empty. |
| API-002 | List available currencies | The API returns EUR as base and stored currencies in ascending order. |
| API-003 | Retrieve rates for a date | The API returns all rates for the latest publication on or before the requested date, or 404 if none exists. |
| API-004 | Retrieve the latest rates | The API returns all rates for the latest publication date with `requested` set to `latest`. |
| API-005 | Convert between currencies | The API converts using exact decimal arithmetic, half-even rounding, and the requested or latest effective date. |
| API-006 | Retrieve currency history | The API returns ordered points and exact decimal summary statistics for the requested range, including an empty result when no points match. |
| API-007 | Reject invalid API requests | Malformed dates or amounts and missing required parameters return 422; unknown currencies and unavailable rates return 404. |

### Feature: Verification

| ID | Story | High-level AC |
|---|---|---|
| VERIFY-001 | Pass the supplied grader | Running the staged grader unfiltered exits zero when every supplied check passes. |
| VERIFY-002 | Pass the automated test suite | Running `bin/test.sh` exits zero only when every automated test passes. |

## Story Guidance

Named stories planning must produce. Authoritative record: `STORY_GUIDANCE.json`.

None.

## Surfaced Acceptance Criteria

| ID | Story ID | Criterion |
|---|---|---|
| AC-001 | CLI-001 | The command-line interface provides help text for each command and sub-verb. |
| AC-002 | API-001 | The API provides a reference or discovery entry point for its routes. |

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
| `sources/INSTRUCTIONS.md` | instruction-to-test | `sources/run.sh` | Instructions identify the harness as the scoring entry point; harness invokes CLI commands and HTTP routes. | Implement command and API behavior before terminal grader verification. |
| `sources/run.sh` | test-kit-to-implementation | CLI operations | Harness runs `init`, `load`, usage-error cases, and `serve`. | CLI stories provide the executable behaviors exercised by the harness. |
| `sources/run.sh` | test-kit-to-implementation | Rates API | Harness checks health, stats, currencies, rates, conversions, history, errors, and live reload. | API stories cover the independently observable route groups and their shared effective-date behavior. |
| `sources/eurofxref-hist_2025-01.csv`, `sources/eurofxref-hist_2025-02-03_04.csv`, `sources/eurofxref-hist_bad.csv` | dependency | CLI-002, VERIFY-001 | The harness loads valid January and February data and rejects the malformed file. | Stage all three fixtures with the grader; use them to verify load behavior. |
| `sources/run.sh` | dependency | VERIFY-001 | The supplied grader is the project acceptance entry point. | Stage and execute it unfiltered as the terminal grader story. |

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

The product is a local command-line loader and JSON HTTP API. CSV history files are the input; SQLite-backed rate records are the shared persisted state; command output and JSON responses are the outputs. The required flow is to initialize the database, load ECB history, start the service, then answer API calls from the stored data. Fetch is an alternate input flow that downloads the ECB archive and loads its history.

### Story Realization Map

| Story ID | Durable Blueprint scope | Evidence | Related files | Requires |
|---|---|---|---|---|
| CLI-001 | Database initialization command | `sources/INSTRUCTIONS.md` — Command line, Database | Persistence library and generated relational layer | capability |
| CLI-002 | Atomic ECB CSV load command | `sources/INSTRUCTIONS.md` — ECB history file rules, Exit codes | Three staged CSV fixtures | capability, acceptance contract |
| CLI-003 | ECB archive fetch command | `sources/INSTRUCTIONS.md` — Command line, Exit codes | Stubbed download in tests | integration, test harness |
| CLI-004 | Local HTTP service command | `sources/INSTRUCTIONS.md` — Command line, HTTP API | FastAPI application | capability |
| CLI-005 | CLI usage and exit behavior | `sources/INSTRUCTIONS.md` — Command line, Exit codes | CLI entry point | capability |
| API-001 | Health and statistics routes | `sources/INSTRUCTIONS.md` — HTTP API | Shared persistence calls | capability |
| API-002 | Currency listing route | `sources/INSTRUCTIONS.md` — HTTP API | Shared persistence calls | capability |
| API-003 | Effective-date rates route | `sources/INSTRUCTIONS.md` — HTTP API, Effective date | Shared persistence calls | capability |
| API-004 | Latest-rates route | `sources/INSTRUCTIONS.md` — HTTP API | Shared persistence calls | capability |
| API-005 | Conversion route | `sources/INSTRUCTIONS.md` — HTTP API, Values | Shared persistence calls | capability |
| API-006 | Currency history route | `sources/INSTRUCTIONS.md` — HTTP API, Values | Shared persistence calls | capability |
| API-007 | API validation and not-found behavior | `sources/INSTRUCTIONS.md` — HTTP API, Errors | API routes | capability |
| VERIFY-001 | Complete supplied grader verification | `sources/run.sh` | All staged grader fixtures and application capabilities | acceptance contract |
| VERIFY-002 | Complete automated test suite verification | `sources/INSTRUCTIONS.md` — Tests | `bin/test.sh`, pytest suite | test harness |

For every persistent read or write, record stable repository-call contracts in `DATABASE.md` under the consuming story ID. Include DTO inputs and outputs; use `data` consumer sensitivity for CLI and API callers. Routes cite call IDs and DTO fields, not database schema or driver details.

### Test and Acceptance Strategy

Keep story tests bounded to the capability being implemented. The terminal grader story runs `sh sources/run.sh` unfiltered and gates on every supplied check passing. The automated test story runs `bin/test.sh` unfiltered and gates on every automated test passing. The Sea Trials also retain these full-run proof gates.

### Sequencing and Dependencies

Build the database initialization and atomic loader before API stories that read persisted rates. Build shared effective-date resolution before rates and conversion routes. Implement the fetch integration against a stubbed download in tests. Build all CLI and API capabilities before either terminal verification story. Stage the grader and its three CSV fixtures before acceptance execution.

### Source Conflicts and Gaps

No unresolved source conflicts or blockers. The project combines CLI and programmatic API signals, so its detected project type is ambiguous. The sources define no human-facing UI.

## Analysis Notes
generated: 2026-10-25
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.184822/workspace/targets/FxRates/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 3
  stories: 15
  stack: Python 3.11+, FastAPI, uvicorn, SQLite, pytest
  display_name: not proposed
  short_description: not proposed

Project type: ambiguous (the source describes both CLI commands and programmatic HTTP API routes).
