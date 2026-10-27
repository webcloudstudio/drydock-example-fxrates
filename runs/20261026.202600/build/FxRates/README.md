# drydock FxRates Uat Case

Drydock uat - FxRates is the web-service kit and the first to exercise FastAPI. The source is an original brief for a currency rates service: a command line loads the European Central Bank euro reference rate history into SQLite, and a FastAPI JSON API serves rates by date (resolved to the latest publication on or before it), conversions between any two currencies with exact decimal rounding, and a currency's history. The supplied grader, sources/run.sh, loads real ECB files for January 2025 plus two February dates, starts the server on a free local port, and makes 35 checks of command output and HTTP status and JSON body. Run with drydock uat FxRates. Source Repo: none, the brief is original to this kit; data from the ECB euro foreign exchange reference rates.

## Intent

Build a currency rates service, an executable named `fxrates` at the application root, as
described in `sources/INSTRUCTIONS.md`. A command line loads the ECB euro reference rate history
into SQLite, and a FastAPI JSON API serves the rates on a date, conversions between any two
currencies, and a currency's history with minimum, maximum, and mean.

Correctness is measured by `sources/run.sh`: it loads the supplied ECB files, starts the server on
a free local port, and makes 35 checks of command output and HTTP status and JSON body. The goal is
every check passing.

## What It Does

Provide the shared FastAPI application entry point used by `uvicorn app_server.main:app` and by in-process acceptance checks.

Give every command a consistent failure contract. Failed commands write no standard output and one diagnostic line to standard error.

Provide the application-root executable `./fxrates`, the `cli.main(argv: list[str] | None = None) -> int` entry point, and the `cli.testing.cli_runner(*args)` helper. Feature stories own command behavior and its implementation.

Convert an amount from one currency to another using ECB rates, with EUR as the base currency.

`GET /currencies` returns EUR as the base and the currencies with at least one stored rate, sorted in ascending order.

`./fxrates fetch` downloads `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip`, extracts `eurofxref-hist.csv`, and passes that file through the same validation, persistence, and reporting workflow as `./fxrates load`.

A download failure returns status 1, writes no standard output, and emits a diagnostic to standard error. Automated tests replace the download with a stub and do not access the network.

Run the supplied grader after all implementation and project test work is complete. The grader's exit status is the release verification result.

`GET /health` provides a lightweight check that the API is responding.

Return a currency's publication points and min, max, and mean statistics over an optional inclusive date range.

`fxrates init` resets the rates store to an empty state. It takes no arguments, prints nothing on success, and uses the persistence boundary.

Return all stored rates for the latest publication date, identifying the request as `latest`.

`./fxrates load <csv>` reads an ECB history file, validates the entire file before its first database write, then stores every rate other than `N/A`. A valid rate replaces the stored value for the same publication date and currency. On success, print CSV output with header `dates,rates` and one data row containing the number of dates with at least one rate and the number of rates stored from this file.

Return the ECB rates for a requested date using the latest available publication on or before that date.

`GET /stats` reports the number of publication dates and stored rates, plus the earliest and latest publication dates. Empty date bounds are null. Values come from repository queries.

Provide a project-owned automated suite that runs locally without network access and exercises the command-line and HTTP product behavior against a real temporary database.

## Stack

Python

## Setup and Running

**Before first run:**

- Confirm the repository has the expected remote with `git remote -v`; add `origin` if the startup guard requires it.
- Run `git status --short` and commit or intentionally stash local changes before deployment-oriented runs.

**Install dependencies:**

```bash
uv sync
```

## Verification

```bash
bash bin/test.sh
```

## Next Steps

- Complete the first-run checks above.
- Run `bash bin/test.sh` before making release or deployment changes.
