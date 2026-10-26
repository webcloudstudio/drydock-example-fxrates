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

Convert an amount from one currency to another. EUR is the base currency with implicit rate one.

Return the stored history for one currency across an inclusive optional date range, with summary statistics.

Allow operators and the supplied harness to initialize an empty rates table before loading history.

Return the rates for the latest publication date on or before a valid requested date. The latest endpoint resolves the most recent stored publication date.

The staged grader is the final end-to-end verification of the complete CLI and HTTP service.

Provide an operator command that downloads and loads the ECB euro reference-rate history archive.

Load ECB historical rates supplied as a CSV file while preserving their published text.

Expose basic service health and a summary of the rates currently stored.

Provide one command that runs the application's pytest suite from the project root. It succeeds only when pytest reports the complete suite passes.

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
