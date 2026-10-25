# Blueprint Analysis: FxRates

## Commander Expectations

- assert the product loads ECB euro reference rates and serves date-based rates, conversions, and currency history through a JSON API
- assert published rate text is preserved and conversions use exact decimal arithmetic
- assert the supplied grader is the acceptance verdict

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: Command Line

| ID | Story | High-level AC |
|---|---|---|
| CLI-001 | Initialize the rates database | `fxrates init` creates an empty rates table and prints nothing. |
| CLI-002 | Load and validate ECB history files | Valid files load idempotently, preserving published rate text; rejected files make no changes and return the specified exit code. |
| CLI-003 | Fetch and load ECB history | `fxrates fetch` downloads and extracts the ECB history file, then loads it using the file-loading rules. |
| CLI-004 | Serve the API on the local port | `fxrates serve` serves on `127.0.0.1` using the requested port or default port. |

### Feature: Rates API

| ID | Story | High-level AC |
|---|---|---|
| API-001 | Report service health and database statistics | `/health` reports the service status; `/stats` reports date and rate counts and date bounds, including an empty database. |
| API-002 | List currencies with stored rates | `/currencies` returns EUR as the base and stored currencies in ascending order. |
| API-003 | Resolve rates by effective publication date | Date and latest requests return the effective publication date, requested date, and that date’s stored rates; requests before the first publication return 404. |
| API-004 | Convert amounts between currencies | `/convert` uses the effective date, validates inputs and currencies, and returns the exact rate and result with the specified rounding. |
| API-005 | Retrieve currency history | `/history` returns bounded, ascending publication points and exact statistics, or the specified empty result; currencies with no stored rates return 404. |

### Feature: Automated Verification

| ID | Story | High-level AC |
|---|---|---|
| TEST-001 | Provide the automated test runner | `bin/test.sh` runs the automated suite and exits zero only when every test passes; fetch tests use a stubbed download and do not open a network connection. |

## Story Guidance

Named stories planning must produce. Authoritative record: `STORY_GUIDANCE.json`.

None.

## Surfaced Acceptance Criteria

| ID | Story ID | Criterion |
|---|---|---|
| AC-001 | CLI-001 | Provide useful command help for each command and subcommand, including usage for invalid invocations. |
| AC-002 | API-003 | Expose a reference or discovery entry point for the programmatic API. |

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
| `sources/INSTRUCTIONS.md` | instruction-to-test | `sources/run.sh` | The brief defines CLI outputs, API responses, error statuses, and expected rate calculations exercised by the harness. | Plan implementation stories against the supplied command and HTTP behavior. |
| `sources/run.sh` | test-kit-to-implementation | CLI and API stories | The staged harness invokes `./fxrates`, loads both ECB fixtures, and calls the local HTTP service. | Stage the harness and fixture files; all referenced entry points must be available at acceptance. |
| ECB history fixtures | dependency | CLI-002 and API stories | The January and February fixtures provide valid rate data; the bad fixture exercises rejection without writes. | Use fixtures to verify loading rules and date-resolution behavior. |
| `sources/INSTRUCTIONS.md` | dependency | TEST-001 | It requires a POSIX-compatible `bin/test.sh`, pytest, a real temporary database, and stubbed fetch. | The test runner and its tests must exercise the product without external network access. |
| `sources/INSTRUCTIONS.md` | dependency | API-001 through API-005 | It defines the response shapes, effective-date rule, exact decimal handling, and error statuses. | Keep endpoint behavior and response values aligned with the normative API contract. |

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

Deliver a local Python command-line application backed by SQLite. The CLI initializes the rates store, loads ECB CSV history, optionally fetches and loads the ECB archive, and starts a FastAPI JSON service on `127.0.0.1`. The API serves health and database statistics, available currencies, effective-date rates, conversions, and bounded currency history. The required flow is initialize, load data, serve, then query; a later load must be visible to the next request. The supplied grader independently exercises CLI behavior and HTTP responses.

### Story Realization Map

| Story ID | Durable Blueprint scope | Evidence | Related files | Capability, integration, migration, test harness, or acceptance contract |
|---|---|---|---|---|
| CLI-001 | Initialization command | `sources/INSTRUCTIONS.md` — Command line | `fxrates` | Capability |
| CLI-002 | CSV parsing, validation, atomic and idempotent load | `sources/INSTRUCTIONS.md` — ECB history file rules; `sources/eurofxref-hist_bad.csv` | ECB CSV fixtures | Capability; acceptance contract |
| CLI-003 | ECB archive download and extraction | `sources/INSTRUCTIONS.md` — `fetch` | Stubbed download in automated tests | Integration |
| CLI-004 | Local API server command | `sources/INSTRUCTIONS.md` — `serve` | FastAPI application | Capability |
| API-001 | Health and aggregate statistics endpoints | `sources/INSTRUCTIONS.md` — HTTP API | FastAPI application | Capability |
| API-002 | Currency catalog endpoint | `sources/INSTRUCTIONS.md` — HTTP API | Loaded rates | Capability |
| API-003 | Effective-date and latest-rate endpoints | `sources/INSTRUCTIONS.md` — Effective date and HTTP API | Loaded rates | Capability |
| API-004 | Exact-decimal conversion endpoint | `sources/INSTRUCTIONS.md` — Values and Errors | Loaded rates | Capability |
| API-005 | Currency history endpoint | `sources/INSTRUCTIONS.md` — HTTP API | Loaded rates | Capability |
| TEST-001 | Automated pytest suite and POSIX runner | `sources/INSTRUCTIONS.md` — Tests | `bin/test.sh`; tests; stubbed fetch | Test harness; acceptance contract |

### Test and Acceptance Strategy

Keep story verification bounded to the command, endpoint, loading rule, or calculation owned by that story. Exercise invalid inputs and not-found cases at their owning boundaries. Test loading against a real temporary database, including atomic rejection and replacement behavior. Stub fetch downloads so automated tests never use the network. Run `sh sources/run.sh` as the final supplied conformance verdict; project-wide acceptance is recorded in SEA_TRIALS.md.

### Sequencing and Dependencies

The database initialization and validated loader underpin API behavior. Implement and verify parsing and loading before rate queries, conversions, and history. Implement the server command with the API routes. Fetch depends on the loader and archive extraction. The automated suite depends on the application capabilities it exercises. The supplied harness and all three CSV fixtures must be staged for final acceptance.

### Source Conflicts and Gaps

No conflicting product definitions or blockers were found. The supplied brief names Python 3.11+, FastAPI, uvicorn, SQLite, and pytest. It requires a shipped persistence library and a generated relational layer from `DATABASE.md`; the technology proposal includes the mandated Python relational stack components. The brief does not define an API reference entry point or exact command-help text; these are surfaced for planning. Authentication is not implied for this local reference-rate service.

## Analysis Notes
generated: 2026-10-24
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.014047/workspace/targets/FxRates/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 3
  stories: 10
  stack: Python 3.11+, FastAPI, uvicorn, SQLite, pytest, SQLAlchemy, Alembic
  display_name: not proposed
  short_description: not proposed

Project type: ambiguous (the sources describe both a command-line interface and programmatic HTTP API routes). No authored COMPASS block is needed because COMPASS.md already exists and is not pending format.
