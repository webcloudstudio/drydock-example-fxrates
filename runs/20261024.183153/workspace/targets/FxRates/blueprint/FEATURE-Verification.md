# FEATURE: Final Verification

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Runs the supplied grader as the final conformance gate for FxRates. |
| Depends On  | ARCHITECTURE.md, DATABASE.md, FEATURE-CLI-Initialize.md, FEATURE-CLI-Load.md, FEATURE-CLI-Fetch.md, FEATURE-CLI-Serve.md, FEATURE-API-Health.md, FEATURE-API-Statistics.md, FEATURE-API-Rates.md, FEATURE-Conversion.md, FEATURE-History.md, FEATURE-Project-Tests.md |
| Provides    | terminal full-suite verification |
| Consumes    | fxrates executable, sources/run.sh |

## Purpose

Run the supplied grader from the application root after all implementation and project-test stories complete. Its exit status is the release conformance verdict.

## Verification workflow

The staged `sources/run.sh` owns the full product check, including the CLI commands, HTTP status codes and JSON bodies. Invoke it without filtering or changing its behavior. This is the terminal story and the only story that runs the complete grader.

## Programmatic Acceptance

=== AC supplied-grader ===
Intent: The supplied grader passes all 35 checks when run against the completed application.

import subprocess

result = subprocess.run(["sh", "sources/run.sh"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC supplied-grader ===

## User Acceptance

- None.

## Guardrails

- Do not modify, rewrite, regenerate, or substitute any file under `sources/`.
- Application code must not read `sources/run.sh` or supplied data files.
