# Blueprint Analysis: drydock FxRates Uat Case

## Commander Expectations

- assert the completed application delivers an executable `fxrates` at the application root that passes `sh sources/run.sh` with exit zero
- assert ECB euro reference rate history files load into SQLite exactly as published and atomically
- assert the service serves rates by effective date, conversions, and currency history over HTTP as JSON
- assert the database is initialized only by `fxrates init` through the generated persistence interface and never by application startup
- assert the test suite runs offline with `fetch` stubbed

## Crew

| Crew | Charge |
|---|---|
| Commander | Defines intent and decides what done means. |
| Team Lead | Confirms epic completeness and stakeholder expectations. |
| Planning Crew | Authors atomic specifications and the ordered Manifest. |
| Shipyard Crew | Builds the tickets without synchronous Commander access. |

## Story List

Summary: features: 6, stories: 24

### Feature: Command-Line Store

| ID | Story | High-level AC |
|---|---|---|
| CLI-001 | Initialize the rates store with `fxrates init` | Creates missing tables and indexes via `persistence.initialize_database(dsn)`; repeated init succeeds and preserves existing rates; exits 0 with no output |
| CLI-002 | Report command usage errors | Unknown command, wrong argument count, or non-integer `--port` exits 2 with a stderr diagnostic and no stdout |
| CLI-003 | Report operational failures | Unreadable file or failed fetch exits 1 with a stderr diagnostic and no stdout |

### Feature: ECB History Loading

| ID | Story | High-level AC |
|---|---|---|
| LOAD-001 | Parse and validate an ECB history CSV | Header `Date` then 3-letter currency codes; trailing empty field ignored; dates valid, unique, `YYYY-MM-DD`; values `N/A` or `[0-9]+(\.[0-9]+)?` nonzero |
| LOAD-002 | Load a validated file atomically | All rows checked before first write; stores every non-N/A rate as text; invalid file exits 3 and stores nothing |
| LOAD-003 | Replace rates on reload | Existing (date, currency) rates replaced; reloading same file leaves database unchanged |
| LOAD-004 | Report load summary | Stdout `dates,rates` then counts of dates with ≥1 stored rate and rates stored |
| LOAD-005 | Fetch ECB history from the official URL | Downloads the zip, extracts `eurofxref-hist.csv`, loads as `load` does; download failure exits 1 |

### Feature: Health and Service Start

| ID | Story | High-level AC |
|---|---|---|
| SVC-001 | Start the HTTP service on a port | `fxrates serve [--port n]` serves on `127.0.0.1:<n>` via uvicorn; default 8000 |
| SVC-002 | Report service health | `GET /health` returns 200 with `{"status": "ok"}` |
| SVC-003 | Serve loads visible to subsequent requests | A load completed while the server runs is visible to the next request |

### Feature: Store Statistics and Currencies

| ID | Story | High-level AC |
|---|---|---|
| STAT-001 | Report store statistics | `GET /stats` returns dates, rates, first, last; first/last null when empty |
| STAT-002 | List stored currencies | `GET /currencies` returns base EUR and ascending currency codes with ≥1 stored rate |

### Feature: Rates by Effective Date

| ID | Story | High-level AC |
|---|---|---|
| RATE-001 | Resolve effective publication date | Request for D uses latest publication ≤ D; 404 when none |
| RATE-002 | Get rates for a date | `GET /rates/{date}` returns effective date, requested date, base EUR, and all rates on effective date as strings |
| RATE-003 | Get latest rates | `GET /rates/latest` returns rates for latest publication with `requested: "latest"` |

### Feature: Currency Conversion

| ID | Story | High-level AC |
|---|---|---|
| CONV-001 | Convert an amount between currencies | `GET /convert` returns date, from, to, amount echoed, rate (6 decimals), result (2 decimals), half-even rounding |
| CONV-002 | Convert using latest publication when date omitted | Without `date`, latest publication date used |
| CONV-003 | Handle conversion errors | Unknown currency or no rate on effective date → 404; malformed amount or missing parameter → 422 |

### Feature: Currency History

| ID | Story | High-level AC |
|---|---|---|
| HIST-001 | Return currency history over a period | `GET /history/{code}` returns count, min, max, mean (6 decimals), points ascending, inclusive optional start/end |
| HIST-002 | Handle empty history | No points yields count 0, null min/max/mean, empty points |
| HIST-003 | Reject history requests with no stored rate | Currency with no stored rate at all, including EUR, returns 404; malformed date returns 422 |

## Story Guidance

Named stories planning must produce. Authoritative record: `STORY_GUIDANCE.json`.

None.

## Surfaced Acceptance Criteria

| ID | Story ID | Criterion |
|---|---|---|
| AC-001 | CLI-001 | `fxrates init` writes nothing to standard output and exits 0 on a fresh database |
| AC-002 | CLI-002 | A failing command writes nothing to standard output and one diagnostic line to standard error |
| AC-003 | LOAD-001 | A row with wrong field count, an invalid or repeated date, or an invalid value rejects the file |
| AC-004 | LOAD-004 | Load output is exactly `dates,rates` followed by the counts line |
| AC-005 | SVC-001 | Server binds only to `127.0.0.1` |
| AC-006 | RATE-002 | Rate values are the stored text, serialized as JSON strings |
| AC-007 | CONV-001 | `result` is computed from stored rates, not from the rounded `rate` |
| AC-008 | HIST-001 | `min` and `max` are the stored text of the smallest and largest rate by value |
| AC-009 | CONV-003 | `/convert` `amount` is echoed exactly as given |

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
| sources/run.sh | instruction-to-test | Command-Line Store, ECB History Loading, Health and Service Start, Rates, Conversion, History | `check` and `http` calls in sources/run.sh | Harness is the acceptance surface; stage verbatim |
| sources/eurofxref-hist_2025-01.csv | reference-to-replacement | LOAD-001, LOAD-002 | Harness loads this file for A2, A3 | Stage as data file |
| sources/eurofxref-hist_2025-02-03_04.csv | reference-to-replacement | LOAD-003, SVC-003 | Harness loads for L1 | Stage as data file |
| sources/eurofxref-hist_bad.csv | reference-to-replacement | LOAD-002 | Harness loads for A4 expecting exit 3 | Stage as data file |
| sources/INSTRUCTIONS.md | instruction-to-test | All stories | Authoritative behavior spec | Prompt-only context |

## Source Roles

| Path | Role | Plan disposition | Build disposition |
|---|---|---|---|
| sources/INSTRUCTIONS.md | author intent | context | prompt-only |
| sources/run.sh | conformance harness | compass | stage |
| sources/eurofxref-hist_2025-01.csv | asset | context | stage |
| sources/eurofxref-hist_2025-02-03_04.csv | asset | context | stage |
| sources/eurofxref-hist_bad.csv | asset | context | stage |

## Planning Instructions

### Delivery Shape

Inferred system: Python 3.11+ CLI plus FastAPI/uvicorn HTTP service over SQLite. Inputs: ECB CSV history files and HTTP requests. Outputs: SQLite rows, stdout/stderr, JSON responses. Execution flow: `init` → `load` → `serve` → HTTP queries. The executable `fxrates` lives at the application root.

### Story Realization Map

- CLI-001..003: `fxrates` entry point, exit codes, `persistence.initialize_database(dsn)` usage. Evidence: INSTRUCTIONS.md Command line; run.sh A1, U1–U4, A5.
- LOAD-001..005: CSV parsing, atomic load, replace-on-reload, summary, fetch with stubbed download. Evidence: INSTRUCTIONS.md ECB history file rules; run.sh A2–A4, L1.
- SVC-001..003: uvicorn serve on 127.0.0.1; health; live visibility. Evidence: run.sh start_server, H1, L2.
- STAT-001..002, RATE-001..003, CONV-001..003, HIST-001..003: endpoint stories. Evidence: run.sh H2–H21, L2–L5.

Each story requires a persistence-backed repository contract (`DATABASE.md`) for `rates` reads/writes.

### Test and Acceptance Strategy

- Focused story tests run `bin/test.sh` slices scoped to the story's pytest module (`Suite: scoped`).
- Terminal verification story (SVC-003 or a dedicated acceptance story) runs `sh sources/run.sh` unfiltered (`Suite: full`) and gates on exit zero.
- Sea Trial st-001 is the sole acceptance verdict.

### Sequencing and Dependencies

- CLI-001 (init) before LOAD-* and SVC-*.
- LOAD-001 → LOAD-002 → LOAD-003 → LOAD-004 → LOAD-005.
- LOAD-002 before RATE-*, STAT-*, CONV-*, HIST-*.
- SVC-001 before SVC-002, SVC-003 and all HTTP endpoint stories.
- Build-before-test: `fxrates` executable before `run.sh` execution.

### Source Conflicts and Gaps

- None. The sources define one coherent behavior set; INSTRUCTIONS.md and run.sh agree on endpoints, status codes, and rounding.

## Analysis Notes
generated: 2026-10-27
blueprint: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/workspace/targets/FxRates/blueprint

Quality: Ready
  blockers: 0
  questions: 0
  features: 6
  stories: 24
  stack: not declared
  display_name: not proposed
  short_description: not proposed

None.
