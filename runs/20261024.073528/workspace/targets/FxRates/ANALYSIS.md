# Blueprint Analysis: FxRates

## Commander Expectations

- assert users can load ECB euro reference rates and retrieve date based rates, conversions, and currency history through a command line and JSON API.

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: Database and ECB Rate Loading

| ID | Story | High-level AC |
|---|---|---|
| DATA-001 | Initialize the rates database | `fxrates init` creates an empty rates table, replacing any existing table. |
| DATA-002 | Load an ECB history file atomically | Valid files store every non-N/A rate as published text, replace matching date and currency rates, and report date and rate counts; rejected files store nothing and return the specified exit code. |
| DATA-003 | Fetch and load ECB history | `fxrates fetch` downloads and loads the ECB history archive using the same validation and reporting behavior as `load`. |

### Feature: Command Line

| ID | Story | High-level AC |
|---|---|---|
| CLI-001 | Run commands and report usage errors | The executable supports the documented commands and arguments, provides command help, and returns the specified usage and operational exit codes. |

### Feature: Rates API

| ID | Story | High-level AC |
|---|---|---|
| API-001 | Serve health, statistics, and currencies | The API returns health status, database summary, and the sorted list of currencies with stored rates. |
| API-002 | Retrieve rates for an effective date | Date and latest requests return all stored rates for the latest publication on or before the requested date, or 404 when none exists. |
| API-003 | Convert between currencies | Conversion returns the effective date, echoed amount, six-decimal half-even rate, and two-decimal half-even result; invalid inputs and unavailable currencies return the specified status. |
| API-004 | Retrieve currency history | History returns points in ascending date order and accurate count, extrema, and six-decimal half-even mean; empty ranges and unavailable currencies follow the specified behavior. |

### Feature: Verification

| ID | Story | High-level AC |
|---|---|---|
| VERIFY-001 | Pass the supplied conformance grader | The unfiltered supplied grader completes successfully, proving every supplied case passes. |

## Story Guidance

Named stories planning must produce. Authoritative record: `STORY_GUIDANCE.json`.

None.

## Surfaced Acceptance Criteria

The analyze step has surfaced these acceptance criteria for `drydock plan` to fold into the relevant story's typed specification.

| ID | Story ID | Criterion |
|---|---|---|
| AC-001 | CLI-001 | The executable provides help text for each command and its supported arguments. |
| AC-002 | API-001 | The service exposes an API reference entry point for its programmatic endpoints. |

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
| `sources/INSTRUCTIONS.md` | instruction-to-test | `sources/run.sh` | The instructions define the CLI and API behavior; the harness checks commands and HTTP responses against known answers. | Implement the specified behaviors and use the staged harness for terminal verification. |
| `sources/run.sh` | test-kit-to-implementation | `fxrates` | The harness invokes the executable, starts the service, and checks its responses. | Deliver an executable at the application root with the required CLI and API. |
| ECB CSV files | dependency | `DATA-002`, `API-002`, `API-003`, `API-004` | The harness loads the January and February files before checking data responses. | Stage the CSV fixtures and load values from persistence rather than embedding answers. |
| `sources/run.sh` | dependency | ECB CSV files | The harness reads the supplied CSV fixtures from its data directory. | Stage the harness and every CSV fixture it reads at the expected paths. |
| `DATA-002` | dependency | `API-001`, `API-002`, `API-003`, `API-004` | API responses are derived from rates loaded into the database. | Complete persistence and loading capabilities before API behavior. |
| `sources/eurofxref-hist_bad.csv` | test-kit-to-implementation | `DATA-002` | The fixture has a valid first row and an invalid second row. | Verify whole-file rejection leaves stored data unchanged. |
| `sources/run.sh` | dependency | `VERIFY-001` | The harness runs the full command and HTTP acceptance flow. | The terminal verification story gates on the complete supplied grader. |

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

Deliver a Python command line that initializes persistence, loads ECB history files, and fetches the ECB archive. It also serves a JSON API over the same database. The execution flow is initialize, load data, serve requests, and verify the complete behavior with the supplied grader. Requests resolve rates from the latest publication on or before the requested date.

### Story Realization Map

| Story ID | Durable Blueprint scope | Evidence | Related files | Capability, integration, migration, test harness, or acceptance contract |
|---|---|---|---|---|
| DATA-001 | Database initialization | `sources/INSTRUCTIONS.md` — Database and Command line | Application entry point and persistence package | Capability |
| DATA-002 | CSV validation, atomic loading, and load reporting | `sources/INSTRUCTIONS.md` — ECB history file rules; `sources/eurofxref-hist_2025-01.csv`; `sources/eurofxref-hist_bad.csv` | CSV loader and persistence package | Capability and integration |
| DATA-003 | ECB archive download and load | `sources/INSTRUCTIONS.md` — Command line fetch | Fetch adapter and CSV loader | Capability and external integration |
| CLI-001 | Executable commands, arguments, help, and exit behavior | `sources/INSTRUCTIONS.md` — Command line and Exit codes | Root `fxrates` executable | Capability |
| API-001 | Health, stats, currencies, and API reference | `sources/INSTRUCTIONS.md` — HTTP API | API application and routes | Capability |
| API-002 | Date and latest rate retrieval | `sources/INSTRUCTIONS.md` — HTTP API effective date and rates | Rates route and persistence calls | Capability |
| API-003 | Decimal currency conversion | `sources/INSTRUCTIONS.md` — HTTP API values and errors | Conversion route and decimal arithmetic | Capability |
| API-004 | Currency history and statistics | `sources/INSTRUCTIONS.md` — HTTP API history and errors | History route and decimal arithmetic | Capability |
| VERIFY-001 | Full supplied-grader verification | `sources/run.sh` | Staged grader and CSV fixtures | Test harness and acceptance contract |

### Test and Acceptance Strategy

Keep implementation checks focused on each story's command, route, validation, and arithmetic behavior. Stub the fetch download in automated tests so they do not open a network connection. Run `sh sources/run.sh` as the single terminal full-suite verification; VERIFY-001 gates on every implementation story and declares `Suite: full`. Final project acceptance is also recorded in SEA_TRIALS.

### Sequencing and Dependencies

Initialize persistence before loading or serving data. Implement CSV validation before fetch integration so fetch can reuse the loader. Complete loading and persistence before API stories. The grader and every fixture it reads must be staged before VERIFY-001 runs. The API must observe completed loads while running.

### Source Conflicts and Gaps

The source describes both a command line and programmatic HTTP routes, so project type signals are mixed. No unresolved source conflict or human-owned decision remains. The source does not define API reference or CLI help behavior; these are surfaced as scoped acceptance criteria.

## Analysis Notes
generated: 2026-10-24
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.073528/workspace/targets/FxRates/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 4
  stories: 9
  stack: Python 3.11+, FastAPI, uvicorn, SQLite, pytest
  display_name: not proposed
  short_description: not proposed

Project type is ambiguous because the sources specify both CLI commands and API routes. No UI screens are described.
