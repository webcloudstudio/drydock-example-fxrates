# Blueprint Analysis: FxRates

## Commander Expectations

- assert the product loads ECB euro reference rates and serves date-based rates, conversions, and currency history through a JSON API.
- assert the command-line loader rejects invalid files without changing stored data.
- assert rates are stored as published text and calculations use exact decimal arithmetic.

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: ECB Rate Data

| ID | Story | High-level AC |
|---|---|---|
| ECB-001 | Initialize the rates store | `fxrates init` drops and recreates an empty rates table. |
| ECB-002 | Load ECB history files | `fxrates load` validates the complete CSV before writing, stores non-`N/A` published rates as text, replaces matching date/currency rates, and reports stored dates and rates. |
| ECB-003 | Fetch and load ECB history | `fxrates fetch` downloads the ECB archive, extracts the history CSV, loads it using the load rules, and reports operational failures. |

### Feature: Rates API

| ID | Story | High-level AC |
|---|---|---|
| API-001 | Serve health and dataset summaries | The service responds with the specified health status, dataset counts and date bounds, and sorted currencies. |
| API-002 | Retrieve rates by effective date | Date and latest requests return the rates for the latest publication on or before the request, or 404 when none exists. |
| API-003 | Convert between currencies | Conversion requests use the requested or latest effective date, exact decimal arithmetic, and the specified rounding and response strings. |
| API-004 | Retrieve currency history | History requests return the selected publication points in ascending order, exact min/max text and six-place mean, or the specified empty result. |

### Feature: Delivery and Verification

| ID | Story | High-level AC |
|---|---|---|
| DEL-001 | Run the application test suite | `bin/test.sh` runs the automated pytest suite and exits zero only when every test passes. |
| DEL-002 | Verify supplied grader conformance | The complete supplied grader passes against the application. |

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
| `sources/INSTRUCTIONS.md` | instruction-to-test | `sources/run.sh` | The instructions define the harness flow and expected behavior; the harness invokes CLI commands and checks HTTP responses. | Use the instructions to shape implementation stories and the staged harness as final conformance verification. |
| `sources/run.sh` | test-kit-to-implementation | Application CLI and API | The harness invokes `./fxrates`, loads the supplied CSVs, starts the server, and checks expected results. | Implement the executable and routes before terminal conformance verification. |
| `sources/eurofxref-hist_2025-01.csv` | fixture-before-verification | ECB loader and rates API | The harness loads this fixture and checks the resulting dataset and API responses. | Stage the fixture and use it in acceptance. |
| `sources/eurofxref-hist_2025-02-03_04.csv` | fixture-before-verification | ECB loader and rates API | The harness loads it while the server runs and checks live visibility and date resolution. | Stage the fixture; implement load visibility for subsequent requests. |
| `sources/eurofxref-hist_bad.csv` | fixture-before-verification | ECB loader | The harness checks rejected-file exit status and atomicity. | Stage the invalid fixture and verify rejection does not partially write. |
| `sources/run.sh` | dependency | `sources/eurofxref-hist_2025-01.csv`, `sources/eurofxref-hist_2025-02-03_04.csv`, `sources/eurofxref-hist_bad.csv` | The harness resolves these fixture files from its source directory. | Stage every referenced CSV at the harness's expected relative paths. |

## Source Roles

| Path | Role | Plan disposition | Build disposition |
|---|---|---|---|
| `sources/INSTRUCTIONS.md` | author intent | prompt-only | none |
| `sources/run.sh` | conformance harness | context | stage |
| `sources/eurofxref-hist_2025-01.csv` | asset | context | stage |
| `sources/eurofxref-hist_2025-02-03_04.csv` | asset | context | stage |
| `sources/eurofxref-hist_bad.csv` | asset | context | stage |

## Planning Instructions

### Delivery Shape

A local command-line loader populates a SQLite rates store from ECB history files. A FastAPI service, served by uvicorn on localhost, reads the store and returns JSON for health, dataset summaries, effective-date rates, conversions, and currency history. The primary flow is initialize, load, serve, and query; fetch provides an additional download-and-load path.

### Story Realization Map

| Story ID | Durable Blueprint scope | Evidence | Related files | Requires |
|---|---|---|---|---|
| ECB-001 | CLI initialization and rates-store setup | `sources/INSTRUCTIONS.md` — Database and Command line | `sources/run.sh` | capability, persistence integration |
| ECB-002 | CSV validation, atomic loading, replacement, and load summary | `sources/INSTRUCTIONS.md` — ECB history file rules; `sources/run.sh` | all three CSV fixtures | capability, persistence integration |
| ECB-003 | ECB archive download, extraction, and load behavior | `sources/INSTRUCTIONS.md` — Command line and fetch rules | None supplied for download | capability, external integration |
| API-001 | Health, stats, and currency routes | `sources/INSTRUCTIONS.md` — HTTP API; `sources/run.sh` | `sources/run.sh` | capability |
| API-002 | Effective-date and latest rates routes | `sources/INSTRUCTIONS.md` — HTTP API; `sources/run.sh` | `sources/run.sh`, CSV fixtures | capability |
| API-003 | Conversion route and decimal rounding | `sources/INSTRUCTIONS.md` — HTTP API values and errors; `sources/run.sh` | `sources/run.sh`, CSV fixtures | capability |
| API-004 | Currency history route and statistics | `sources/INSTRUCTIONS.md` — HTTP API values and errors; `sources/run.sh` | `sources/run.sh`, CSV fixtures | capability |
| DEL-001 | Automated pytest suite and POSIX test runner | `sources/INSTRUCTIONS.md` — Tests | None supplied | test harness |
| DEL-002 | Complete supplied grader verification | `sources/INSTRUCTIONS.md` — Run Harness; `sources/run.sh` | `sources/run.sh`, all CSV fixtures | acceptance contract |

### Test and Acceptance Strategy

Each feature story receives focused tests for its own observable behavior using temporary databases. Fetch tests stub the download and must not open a network connection. The terminal verification story runs the complete supplied harness, `sh sources/run.sh`, after all implementation stories. The project-level Sea Trial records that same full conformance gate.

### Sequencing and Dependencies

Create the persistence boundary and CLI initialization before file loading. Implement CSV validation and atomic writes before fetch delegates to the loader. Complete persistence and route behavior before API verification. The test runner and focused tests accompany their owned capabilities; terminal conformance follows all implementation stories. Stage the harness and every CSV fixture it opens. No migrations are required by the source, which describes a one-table schema created by initialization.

### Source Conflicts and Gaps

The source describes a programmatic API and a CLI, with no human-facing screens; project type is therefore `ambiguous`. No unresolved conflicting product definitions or human-owned planning questions were found. Deployment beyond localhost operation is unspecified and not needed to build the stated product.

## Analysis Notes
generated: 2026-10-25
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/workspace/targets/FxRates/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 3
  stories: 9
  stack: Python 3.11+, FastAPI, uvicorn, SQLite, pytest
  display_name: not proposed
  short_description: not proposed

Project type: ambiguous (CLI commands and programmatic HTTP API are both described).
