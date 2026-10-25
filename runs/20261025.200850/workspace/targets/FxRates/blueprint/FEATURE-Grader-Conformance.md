# FEATURE: Grader Conformance

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Defines final conformance verification against the supplied FxRates grader. |
| Depends On  | ARCHITECTURE.md, DATABASE.md, FEATURE-API-Foundation.md, FEATURE-CLI-Foundation.md, FEATURE-Store-Initialization.md, FEATURE-ECB-Loading.md, FEATURE-ECB-Fetch.md, FEATURE-Dataset-Summary.md, FEATURE-Effective-Rates.md, FEATURE-Currency-Conversion.md, FEATURE-Currency-History.md, FEATURE-Test-Runner.md |
| Provides    | supplied grader conformance |
| Consumes    | fxrates init, fxrates load, fxrates serve, GET /health, GET /stats, GET /currencies, GET /rates/{date}, GET /rates/latest, GET /convert, GET /history/{code} |

## Purpose

This is the terminal verification capability. It runs the supplied read-only grader after the implementation stories are complete. The grader loads the staged ECB fixtures, exercises the CLI and API, and its exit status is the final conformance verdict.

## Verification Contract

- Run `sh sources/run.sh` from the completed application root.
- The runner starts with a fresh temporary SQLite database, invokes `fxrates init` and `fxrates load`, starts the local server, and checks command exit codes and standard output plus HTTP status and JSON values.
- The suite covers command usage errors, valid and invalid loads, effective-date lookups, conversions, history summaries, and visibility of a load performed while the server is running.
- No application code reads the grader or hardcodes its answers.

## Programmatic Acceptance

=== AC supplied-grader-full ===
Intent: The complete authoritative supplied grader passes all 35 command and HTTP checks.
Suite: full

import subprocess

result = subprocess.run(
    ["sh", "sources/run.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC supplied-grader-full ===

## User Acceptance

- None.

## Guardrails

- Treat the supplied grader and fixture files as read-only staged assets.
- Do not copy its answers into application code or read `sources/run.sh` from application code.
- Run the full grader only in this terminal verification story after the other stories close.
