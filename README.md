# FxRates

A Drydock UAT kit that builds a FastAPI currency rates service over SQLite from real ECB data. The
brief is original to this kit. Complexity: 3 of 5, about 7 stories.

| Path | Role |
|---|---|
| `sources/INSTRUCTIONS.md` | The specification imported into the Target. |
| `sources/eurofxref-hist_2025-01.csv` | ECB history, January 2025: 22 dates, 8 currencies, an all-`N/A` `HRK` column. ECB format, newest first, trailing commas. |
| `sources/eurofxref-hist_2025-02-03_04.csv` | Two further dates, loaded while the server runs. |
| `sources/eurofxref-hist_bad.csv` | Valid row then an invalid rate (`1.0x`); the load must store nothing. |
| `bin/run.sh` | The grader. Staged into the build as `sources/run.sh`; `acceptance.full` runs it. |
| `tools/` | `fxrates.py` (a standard-library reference with the same contract), `emit_fx.py` and `fx_checks.txt` (produced the answers). Not imported. |
| `inputs/` | Frozen `SEA_TRIALS.md`, `TECHNOLOGY_STACK.md`, `COMPASS.md`, `METADATA.md`. |

## Grading

`bin/run.sh [APP]` grades the configured, schema-provisioned test store. It preserves
`DATABASE_URL`, falls back to `DATABASE_PATH`, then `data/app.db` relative to APP. A missing store
or `rates` table fails preflight without creating a database. The DATABASE step owns schema
creation; `init` only empties the table. The grader clears existing rates and leaves its loaded
fixture rows in place, so the configured store must be dedicated to testing. Agent calls use
the provisioned test store supplied by Drydock.

The grader runs `APP/fxrates` (default: the current directory), starts
`fxrates serve --port <free port>`, and makes the same 35 checks. HTTP
bodies are compared as JSON values; error bodies are not compared. The server is stopped on exit.

| Group | Checks |
|---|---|
| A | `init`; load January twice (idempotent); rejected file; missing file |
| U | command-line usage errors |
| H | `/health`, `/stats`, `/currencies`, `/rates` on a weekday, a Saturday, before the data, malformed, `latest`; `/convert` cross, from EUR on a Sunday, to EUR, unknown currency, missing and malformed amount, before the data; `/history` with ranges, the all-`N/A` currency, an empty range, a malformed date |
| L | load February while serving; `/stats`, `latest`, a weekend lookup, history across the month boundary |

The server must answer `GET /health` within 30 seconds of starting, or the run stops with the
HTTP checks unscored.

## Data traps

`HRK` appears in the header but has no rates, so it is absent from `/currencies` and `/history/HRK`
is `404`. The ECB drops trailing zeros (`0.943`), and the API returns rates as published text. No
conversion, rate, or mean in the exam lands on a rounding tie, so half-even and half-up agree.
Python is needed on `PATH` to run the grader's HTTP checks; it uses the standard library only.
