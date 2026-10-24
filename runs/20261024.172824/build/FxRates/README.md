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

CLI usage errors, rejected files, and operational failures use the exit statuses declared for each condition. Every failed command writes no standard output and one diagnostic line to standard error. `bin/test.sh` runs the project pytest suite from the application root.

Convert between any two currencies using EUR as the base. If no date is supplied, use the latest publication. If a date is supplied, resolve it to the latest publication on or before that date.

Return the EUR base and every currency with at least one stored rate, sorted by currency code in ascending order.

Fetch the ECB history archive, extract `eurofxref-hist.csv`, and load its data under the same validation, atomicity, storage, and counting rules as `fxrates load`.

Expose health and aggregate store statistics through JSON endpoints.

Return the stored rates for a currency in ascending publication-date order, with optional inclusive `start` and `end` date bounds. Report count, minimum, maximum, and exact mean. The minimum and maximum are the stored text for the values selected by numeric value. The mean is rounded half to even to six decimal places and returned as a string with exactly six decimal places.

If the range has no points, return count zero, null statistics, and an empty points list. Return 404 if the currency has no stored rate at all, including EUR. Malformed date bounds return 422.

`fxrates init` drops and recreates the `rates` table empty, using the configured database location and the generated persistence boundary.

Load a local ECB history CSV into the configured rates store. Validate the entire file before the first write. A rejected file must leave the store unchanged.

Return all rates stored for the latest publication on or before the requested date. EUR is the base and has an implicit rate of 1; only currencies with stored rates appear in the response.

`./fxrates serve [--port <n>]` runs the HTTP API in the foreground on `127.0.0.1`. The default port is `8000`. The process stays running until stopped and shuts down cleanly on SIGTERM.

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
