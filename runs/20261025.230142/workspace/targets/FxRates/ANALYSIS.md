# Blueprint Analysis: FxRates

## Commander Expectations

- assert users can load ECB euro reference rate history and retrieve rates, conversions, and currency history through a command line and JSON API

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: Rate Data Loading

| ID | Story | High-level AC |
|---|---|---|
| LOAD-001 | Initialize the rates store | `fxrates init` creates an empty rates table, replacing any existing table. |
| LOAD-002 | Load and validate ECB history files | Valid CSV rows load atomically; published rates retain their text, `N/A` values are skipped, duplicate date/currency rates are replaced, and output reports dates and rates stored. |
| LOAD-003 | Fetch and load ECB history | `fxrates fetch` downloads and extracts the ECB history file, then loads it using the same validation and reporting rules. |

### Feature: Rates API

| ID | Story | High-level AC |
|---|---|---|
| API-001 | Serve API health and reference data | The service returns the specified health, database statistics, and sorted currencies responses. |
| API-002 | Retrieve rates by effective date | Date and latest requests return rates for the latest publication on or before the requested date, or 404 when none exists. |
| API-003 | Convert amounts between currencies | Conversion uses exact decimal arithmetic, applies the specified rounding, and returns the effective date and formatted values. |
| API-004 | Retrieve currency history | History returns ordered points and the specified count, min, max, and mean for optional inclusive date bounds. |
| API-005 | Validate API requests and report errors | Malformed dates, amounts, and missing required parameters return 422; unknown or unavailable currencies and dates return 404. |
| API-006 | Run the service on the configured local port | `fxrates serve` starts the API on `127.0.0.1` at the requested or default port. |

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
| `sources/INSTRUCTIONS.md` | instruction-to-test | `sources/run.sh` | The instructions define the CLI, API, database behavior, and expected errors; the harness checks command output and HTTP responses. | Use the instructions to plan behavior; stage and execute the harness as the final conformance check. |
| `sources/run.sh` | test-kit-to-implementation | `fxrates` CLI and API | The harness invokes `init`, `load`, and `serve`, then checks API responses. | Implement the executable and service capabilities before the terminal verification story. |
| `sources/eurofxref-hist_2025-01.csv` | dependency | `LOAD-002` | The harness loads this fixture and expects January rates. | Stage the fixture with the harness. |
| `sources/eurofxref-hist_2025-02-03_04.csv` | dependency | `LOAD-002` and `API-002`/`API-004` | The harness loads these dates while the server runs and checks updated statistics, latest rates, date resolution, and history. | Stage the fixture and ensure subsequent requests see completed loads. |
| `sources/eurofxref-hist_bad.csv` | dependency | `LOAD-002` | The harness expects this file to be rejected. | Stage the invalid fixture for atomic-rejection verification. |

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

A local Python command line initializes the SQLite rates store, validates and loads ECB CSV data, and supports fetching the current history archive. A FastAPI JSON service runs on localhost and serves health, statistics, currencies, effective-date rates, conversions, and currency history. The flow is initialization, CSV load (or fetch), then serving requests; a load completed during service is visible to the next request.

### Story Realization Map

| Story ID | Durable Blueprint scope(s) | Evidence | Related files | Requires |
|---|---|---|---|---|
| LOAD-001 | CLI initialization | `sources/INSTRUCTIONS.md` Database and Command line sections | `fxrates` | capability |
| LOAD-002 | Atomic ECB CSV validation and loading | `sources/INSTRUCTIONS.md` ECB history file rules; `sources/run.sh` A2–A5 and L1 | `sources/eurofxref-hist_2025-01.csv`, `sources/eurofxref-hist_2025-02-03_04.csv`, `sources/eurofxref-hist_bad.csv` | capability, integration |
| LOAD-003 | ECB archive fetch and load | `sources/INSTRUCTIONS.md` Command line and fetch rules | `fxrates` | capability, integration |
| API-001 | Health, stats, and currencies endpoints | `sources/INSTRUCTIONS.md` HTTP API; `sources/run.sh` H1–H3 | `sources/run.sh` | capability |
| API-002 | Effective-date and latest rates endpoints | `sources/INSTRUCTIONS.md` HTTP API effective date; `sources/run.sh` H4–H8, L3–L4 | `sources/run.sh` | capability |
| API-003 | Currency conversion endpoint | `sources/INSTRUCTIONS.md` HTTP API values and errors; `sources/run.sh` H9–H16 | `sources/run.sh` | capability |
| API-004 | Currency history endpoint | `sources/INSTRUCTIONS.md` HTTP API values and errors; `sources/run.sh` H17–H21, L5 | `sources/run.sh` | capability |
| API-005 | API validation and error behavior | `sources/INSTRUCTIONS.md` HTTP API errors; `sources/run.sh` H6–H7, H13–H16, H19, H21 | `sources/run.sh` | capability |
| API-006 | Service startup and local binding | `sources/INSTRUCTIONS.md` Command line; `sources/run.sh` startup probe | `fxrates` | capability, integration |

### Test and Acceptance Strategy

Keep each implementation story's tests focused on its command or endpoint behavior, using temporary databases and a stubbed fetch download. Run the supplied unfiltered `sources/run.sh` once as the terminal verification gate after all implementation stories; its exit status proves every supplied case passes. The harness itself uses the network only for requests to the local service, while fetch tests use a stub.

### Sequencing and Dependencies

Implement the rates persistence boundary and schema as foundations for loading and API stories. LOAD-001 precedes LOAD-002; LOAD-003 depends on the shared loader. API stories depend on persisted rates and the service startup capability. API-005 validation should be exercised alongside each endpoint and consolidated after route behavior exists. The terminal verification story depends on every implementation story. Stage the harness and all three CSV fixtures before acceptance runs.

### Source Conflicts and Gaps

The source describes the product as a local service and names Python 3.11+, FastAPI, uvicorn, SQLite, pytest, and TestClient. The database instructions also require all database access to go through the shipped persistence library and generated relational layer; preserve that boundary in planning. Authentication, authorization, deployment beyond localhost, and help-text details are not specified; none prevents the stated local command-line/API workflow.

## Analysis Notes
generated: 2026-10-25
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.230142/workspace/targets/FxRates/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 2
  stories: 9
  stack: Python 3.11+, FastAPI, uvicorn, SQLite, pytest, TestClient
  display_name: not proposed
  short_description: not proposed

None.
