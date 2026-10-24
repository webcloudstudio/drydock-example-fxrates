# Blueprint Analysis: FxRates

## Commander Expectations

- assert users can load ECB euro reference rates and retrieve rates, conversions, and currency history through a JSON API
- assert invalid history files leave the database unchanged
- assert the supplied grader passes

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

### Feature: Rate Data Management

| ID | Story | High-level AC |
|---|---|---|
| DATA-001 | Initialize the rates database | `fxrates init` creates an empty rates table and prints nothing. |
| DATA-002 | Load ECB history files | `fxrates load` validates the entire file before writing, stores published rate text, replaces matching date/currency rates, and reports date and rate counts. |
| DATA-003 | Fetch ECB history | `fxrates fetch` downloads and extracts the ECB history file, loads it using the same validation and persistence behavior, and reports the load counts. |

### Feature: Rates API

| ID | Story | High-level AC |
|---|---|---|
| API-001 | Serve health and dataset summaries | The service returns the specified health, statistics, and sorted currency JSON responses. |
| API-002 | Retrieve rates by effective date | Date and latest requests return all rates for the latest publication on or before the requested date; requests before the first publication return 404. |
| API-003 | Convert between currencies | Conversion returns the effective date, echoed amount, six-decimal half-even rate, and two-decimal half-even result; missing rates return 404. |
| API-004 | Retrieve currency history | History returns inclusive, ascending points and exact statistics; a currency with no stored rates returns 404. |

### Feature: Delivery and Verification

| ID | Story | High-level AC |
|---|---|---|
| DEL-001 | Provide the test runner | `bin/test.sh` runs the application’s pytest suite and exits zero only when every test passes; fetch tests stub downloads and use no network. |
| DEL-002 | Pass the supplied grader | The complete supplied grader exits zero against the application and its HTTP responses. |

## Story Guidance

Named stories planning must produce. Authoritative record: `STORY_GUIDANCE.json`.

None.

## Surfaced Acceptance Criteria

| ID | Story ID | Criterion |
|---|---|---|
| AC-001 | DATA-003 | Tests replace the download with a stub and make no network connection. |

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
| `sources/INSTRUCTIONS.md` | instruction-to-test | `sources/run.sh` | The instructions identify the harness as the scoring entry point and describe its command and API checks. | Implement the specified command and API behaviors; use the staged harness as final conformance verification. |
| `sources/run.sh` | test-kit-to-implementation | CLI and API stories | The harness invokes `./fxrates`, loads the staged CSV files, and requests the local HTTP API. | The executable, database, and server must work together from the application root. |
| `sources/eurofxref-hist_2025-01.csv` | dependency | DATA-002, API stories | The harness loads this file and expects its stored rates in API responses. | Stage the fixture and preserve its published values as text. |
| `sources/eurofxref-hist_2025-02-03_04.csv` | dependency | DATA-002, API stories | The harness loads it while the service is running and then checks updated responses. | Support visible updates on subsequent requests. |
| `sources/eurofxref-hist_bad.csv` | dependency | DATA-002 | The harness uses the valid first row and invalid second row to check rejection. | Validate the full file before any write. |
| Shipped persistence library and generated relational layer | dependency | DATA-001, DATA-002, API-001–API-004 | Instructions require all database access to go through the shipped library and generated layer. | Database reads and writes use the stable repository contracts authored in `DATABASE.md`; API stories consume DTOs rather than database details. |
| `sources/run.sh` | reference-to-replacement | `bin/test.sh` and application behavior | The supplied harness is the acceptance grader; instructions separately require an application pytest runner. | Keep the grader staged and unchanged; provide the project’s own network-free test runner. |

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

Build a local command-line application that initializes a SQLite database, loads or fetches ECB history, and serves a JSON API on `127.0.0.1`. The API reads the persisted rates and returns health, dataset summaries, effective-date rates, exact-decimal conversions, and currency histories. The required flow is initialize, load data, start the server, then query it. Fetch is a separate network-backed command; its tests use a stubbed download.

### Story Realization Map

| Story ID | Durable Blueprint scope | Evidence | Related files and realization |
|---|---|---|---|
| DATA-001 | CLI database initialization | `sources/INSTRUCTIONS.md` | Application entry point and generated persistence layer; capability. |
| DATA-002 | CSV validation and transactional loading | `sources/INSTRUCTIONS.md`, `sources/eurofxref-hist_2025-01.csv`, `sources/eurofxref-hist_bad.csv` | Parser, persistence calls, and CSV fixtures; capability and focused tests. |
| DATA-003 | ECB archive fetch and load | `sources/INSTRUCTIONS.md` | Download/extraction integration reuses DATA-002; stubbed download tests. |
| API-001 | Health, stats, and currencies routes | `sources/INSTRUCTIONS.md`, `sources/run.sh` | FastAPI routes and persistence read contracts; capability and route tests. |
| API-002 | Effective-date and latest rates routes | `sources/INSTRUCTIONS.md`, `sources/run.sh` | FastAPI routes and persistence read contract; capability and route tests. |
| API-003 | Exact-decimal conversion route | `sources/INSTRUCTIONS.md`, `sources/run.sh` | FastAPI route, Decimal arithmetic, and persistence read contract; capability and route tests. |
| API-004 | Currency history route and statistics | `sources/INSTRUCTIONS.md`, `sources/run.sh` | FastAPI route, Decimal statistics, and persistence read contract; capability and route tests. |
| DEL-001 | POSIX pytest runner and application test suite | `sources/INSTRUCTIONS.md` | `bin/test.sh`, pytest suite, temporary database, and stubbed fetch; test harness. |
| DEL-002 | Complete supplied grader verification | `sources/run.sh`, fixtures | Terminal verification depends on every implementation story; acceptance contract. |

### Test and Acceptance Strategy

Use focused pytest coverage for each command, loader rule, route, effective-date behavior, rounding rule, and error status. Stub fetch downloads so tests open no network connection. Run the supplied grader only as the terminal full conformance gate after implementation is complete. Sea Trial `st-001` records that gate; `st-002` records the application test runner requirement.

### Sequencing and Dependencies

Author the relational repository contracts before stories that read or write persistent data. Build the parser and transactional loader before fetch integration. Implement persistence and data loading before API routes. Provide fixtures and focused tests with the capabilities they verify. Complete the application test runner and all implementation stories before terminal grader verification.

### Source Conflicts and Gaps

No unresolved cross-source conflicts or human-owned product decisions are present. The source specifies both CLI and programmatic HTTP API behavior, so project type is mixed (`ambiguous`). The local server binding and data behavior are specified; no human-user screens or protected resources are described.

## Analysis Notes
generated: 2026-10-24
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.151448/workspace/targets/FxRates/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 3
  stories: 9
  stack: Python 3.11+, FastAPI, uvicorn, SQLite, pytest, FastAPI TestClient
  display_name: not proposed
  short_description: not proposed

Project type: ambiguous (CLI commands and programmatic HTTP routes are both described). `TECHNOLOGY_STACK.md` includes the relational persistence selections required for Python targets.
