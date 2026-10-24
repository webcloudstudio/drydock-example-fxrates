# FEATURE: Release Verification

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Runs the supplied end-to-end grader as the final release verification. |
| Depends On  | ARCHITECTURE.md, DATABASE.md, FEATURE-API-Foundation.md, FEATURE-CLI-Foundation.md, FEATURE-ECB-Init.md, FEATURE-ECB-Load.md, FEATURE-ECB-Fetch.md, FEATURE-API-Stats.md, FEATURE-API-Health.md, FEATURE-API-Rates.md, FEATURE-API-Convert.md, FEATURE-API-History.md, FEATURE-API-Validation.md, FEATURE-CLI-Serve.md, FEATURE-CLI-Errors.md, FEATURE-Verification-Suite.md |
| Provides    | full supplied grader acceptance |
| Consumes    | ./fxrates |

## Purpose

Run the staged conformance harness from the application root after all implementation stories and the project test suite are complete. The harness initializes a fresh database, loads the supplied ECB fixtures, starts the API, and checks command output, HTTP status codes, and JSON bodies.

## Workflow

1. Invoke `sh sources/run.sh` from the application root.
2. Require exit status zero, which means every check in the supplied grader passed.

## Guardrails

- Do not modify, rewrite, regenerate, or substitute any file under `sources/`.
- Do not run this whole-project grader before the terminal verification story.
- Treat the grader’s exit status as the verdict; its output is diagnostic.
- The grader uses only local HTTP requests and does not run `fetch`.

## Programmatic Acceptance

=== AC supplied-grader ===
Intent: The complete supplied grader passes against the finished application.
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
=== END AC supplied-grader ===

## User Acceptance

- None.

## Guardrails

- Do not modify, rewrite, regenerate, or substitute any file under `sources/`.
- Keep the supplied grader as the final project verification gate.
