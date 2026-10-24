# FEATURE: Verification

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines the final verification commands for the completed FxRates application. |
| Depends On  | FEATURE-CLI-Usage.md, FEATURE-Serve.md |
| Provides    | bin/test.sh, supplied FxRates grader |
| Consumes    | pytest suite, sources/run.sh |

## Purpose

The completed application provides `bin/test.sh`, a POSIX-compatible launcher that runs the project's pytest suite from the application root and succeeds only when every test passes. The supplied `sources/run.sh` is an authoritative full-project grader. This story is the terminal full-suite gate, after all implementation stories are complete.

The grader sets `DATABASE_URL` to a fresh temporary SQLite file, exercises CLI commands, starts the local server, and checks its HTTP responses. It does not exercise `fetch` and makes no network requests beyond localhost.

## Verification behavior

Keep the supplied grader and its CSV fixtures unchanged. The full grader is run only by this terminal story. The project's test suite covers each command, each CSV load rule, each endpoint, effective-date selection, rounding, and error statuses; tests of `fetch` stub the download and use no network.

## Programmatic Acceptance

=== AC terminal-grader ===
Intent: The supplied end-to-end grader passes against the completed application.
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
=== END AC terminal-grader ===

=== AC pytest-launcher ===
Intent: The project's POSIX test launcher runs the complete pytest suite successfully.

import subprocess

result = subprocess.run(
    ["sh", "bin/test.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC pytest-launcher ===

## User Acceptance

- None.

## Guardrails

- Do not modify, rewrite, regenerate, or substitute files under `sources/`.
- Automated tests stub ECB downloads and never use the network.
- The supplied grader is run as the terminal full-suite acceptance gate.
