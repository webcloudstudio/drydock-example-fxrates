# FEATURE: Supplied Grader Verification

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Runs the supplied grader as the final conformance check for FxRates. |
| Depends On  | FEATURE-CLI-Init.md, FEATURE-CLI-Load.md, FEATURE-CLI-Serve.md, FEATURE-API-Overview.md, FEATURE-API-Rates.md, FEATURE-API-Convert.md, FEATURE-API-History.md |
| Provides    | supplied grader verification |

## Purpose

The supplied `sources/run.sh` harness is the authoritative final conformance gate. It exercises the command output, HTTP statuses, and JSON values defined by the source specification.

## Workflow

Run the grader from the application root using `sh sources/run.sh` after all implementation and project-test work is complete. Preserve the supplied grader and data files verbatim. Its exit status is the verdict.

This story is the terminal full-suite verification.

## Guardrails

- Do not modify, rewrite, regenerate, or substitute any file under `sources/`.
- Do not run this final grader as an intermediate story check.

## Programmatic Acceptance

=== AC supplied-grader-full ===
Intent: The supplied end-to-end grader passes every check after all capabilities are assembled.
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

- None.
