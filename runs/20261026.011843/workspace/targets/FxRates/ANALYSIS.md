# Blueprint Analysis: FxRates

## Commander Expectations

- assert the product loads ECB euro reference rates and serves date-based rate, conversion, and history queries through a JSON API.

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: Database and ECB Data Loading

| ID | Story | High-level AC |
|---|---|---|
| DATA-001 | Initialize the rates database | `fxrates init` creates an empty rates table, replacing any existing table. |
| DATA-002 | Load an ECB history file | Valid rows load atomically; published rate text is preserved, N/A values are skipped, matching records are replaced, and date and rate totals are reported. |
| DATA-003 | Fetch and load ECB history | `fxrates fetch` downloads and extracts the ECB history file, loads it using the history-file rules, and reports operational download failures. |

### Feature: Rates API

| ID | Story | High-level AC |
|---|---|---|
| API-001 | Serve health, statistics, and currencies | The API reports health, database date and rate totals, and the ascending list of currencies with stored rates. |
| API-002 | Resolve rates by effective date | Date and latest requests return all rates on the latest publication date on or before the requested date, or 404 if none exists. |
| API-003 | Convert between currencies | The API returns the effective date, echoed amount, six-place rounded rate, and two-place rounded result using exact decimal arithmetic. |
| API-004 | Report currency history | The API returns ascending date and rate points with count, minimum, maximum, and six-place rounded mean; empty periods return null statistics and no points. |

### Feature: Verification

| ID | Story | High-level AC |
|---|---|---|
| QA-001 | Provide an automated test runner | `bin/test.sh` exits zero only when every automated test passes; tests use a stubbed fetch download and no network connection. |
| QA-002 | Pass the supplied end-to-end grader | The unfiltered supplied grader completes successfully against the application. |

## Story Guidance

Named stories planning must produce. Authoritative record: `STORY_GUIDANCE.json`.

None.

## Surfaced Acceptance Criteria

| ID | Story ID | Criterion |
|---|---|---|
| AC-001 | DATA-001 | Each CLI command and subcommand provides usable help text. |

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
| `sources/INSTRUCTIONS.md` | instruction-to-test | `sources/run.sh` | The instructions define the command and API behaviors checked by the grader. | Implement the specified observable behavior and use the grader as the terminal end-to-end check. |
| `sources/eurofxref-hist_2025-01.csv`, `sources/eurofxref-hist_2025-02-03_04.csv` | fixture-before-verification | `sources/run.sh` | The grader loads both files and checks counts, rates, and effective-date behavior. | Stage both fixtures for grader execution. |
| `sources/eurofxref-hist_bad.csv` | fixture-before-verification | `sources/run.sh` | The grader checks rejection of an invalid rate. | Stage the invalid fixture to verify atomic rejection. |
| `sources/INSTRUCTIONS.md` | dependency | `sources/run.sh` | The instructions require `bin/test.sh` and a stubbed fetch test; the grader itself does not run fetch. | Provide a separate offline automated test runner and stub download behavior in its tests. |
| `sources/run.sh` | test-kit-to-implementation | `fxrates` | The grader invokes CLI commands, starts the service, and checks HTTP responses. | The executable and API must be ready before the terminal grader story runs. |

## Source Roles

| Path | Role | Plan disposition | Build disposition |
|---|---|---|---|
| `sources/INSTRUCTIONS.md` | normative specification and conformance test suite | context | prompt-only |
| `sources/eurofxref-hist_2025-01.csv` | asset | context | stage |
| `sources/eurofxref-hist_2025-02-03_04.csv` | asset | context | stage |
| `sources/eurofxref-hist_bad.csv` | asset | context | stage |
| `sources/run.sh` | conformance harness | context | stage |

## Planning Instructions

### Delivery Shape

Build a Python command-line application and a local FastAPI JSON service backed by SQLite. The CLI initializes the database, loads ECB CSV history, and fetches and loads the ECB archive. The service exposes health, statistics, currencies, effective-date rates, conversions, and currency history. The delivery flow is database initialization, file loading, API service, focused automated tests, then the supplied end-to-end grader.

### Story Realization Map

| Story ID | Durable Blueprint scope | Evidence | Related files | Capability |
|---|---|---|---|---|
| DATA-001 | Database initialization and CLI usage | `sources/INSTRUCTIONS.md` | `fxrates`, database configuration | CLI capability |
| DATA-002 | Atomic CSV validation, load, replacement, and reporting | `sources/INSTRUCTIONS.md`, `sources/eurofxref-hist_bad.csv` | valid and invalid CSV fixtures | Import capability |
| DATA-003 | ECB archive fetch, extraction, and load | `sources/INSTRUCTIONS.md` | stubbed download test | External integration |
| API-001 | Health, stats, and currency endpoints | `sources/INSTRUCTIONS.md`, `sources/run.sh` | grader HTTP checks | API capability |
| API-002 | Effective-date and latest-rate endpoints | `sources/INSTRUCTIONS.md`, `sources/run.sh` | January and February fixtures | API capability |
| API-003 | Exact decimal conversion endpoint | `sources/INSTRUCTIONS.md`, `sources/run.sh` | loaded rates | API capability |
| API-004 | Currency history endpoint and summary statistics | `sources/INSTRUCTIONS.md`, `sources/run.sh` | loaded rates | API capability |
| QA-001 | Offline automated test runner | `sources/INSTRUCTIONS.md` | test suite and fetch stub | Test harness |
| QA-002 | Complete supplied grader verification | `sources/run.sh` | all implementation stories and staged fixtures | Acceptance contract |

### Test and Acceptance Strategy

Write focused tests for each CLI operation, CSV acceptance and rejection rule, endpoint, date resolution, rounding behavior, and error status. The `bin/test.sh` story runs the project's automated suite with fetch stubbed and no network. The terminal grader story runs `sh sources/run.sh` unfiltered. Project-wide acceptance, including the complete supplied grader and prohibition on test network access, is recorded in Sea Trials.

### Sequencing and Dependencies

Initialize the database before load and API behavior. CSV validation and atomic persistence underpin both CLI loading and fetch. Fetch uses the same load behavior after download and extraction. API stories depend on persisted rates. The automated suite follows implementation, and the supplied grader is the terminal verification story. The relational Python stack proposal includes the persistence components required by the Blueprint workflow.

### Source Conflicts and Gaps

No conflicting product definitions or blockers. The unattended UAT policy prohibits questionnaires and open questions; identity is derived from the supplied project description.

## Analysis Notes
generated: 2026-10-25
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.011843/workspace/targets/FxRates/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 3
  stories: 9
  stack: Python 3.11+, FastAPI, uvicorn, SQLite, pytest
  display_name: not proposed
  short_description: not proposed

Project type is mixed API and CLI, classified as ambiguous. The sources specify no human-facing screens. The COMPASS already exists and was not regenerated.
