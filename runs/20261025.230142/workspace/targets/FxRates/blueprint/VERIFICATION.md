# FEATURE: Release Verification

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Run the completed project test suite and supplied conformance grader. |
| Depends On  | FEATURE-InitializeRates.md, FEATURE-LoadHistory.md, FEATURE-FetchHistory.md, FEATURE-ApiReference.md, FEATURE-EffectiveRates.md, FEATURE-Convert.md, FEATURE-CurrencyHistory.md, FEATURE-ApiErrors.md, FEATURE-Serve.md |
| Provides    | bin/test.sh, release conformance verification |
| Consumes    | pytest suite, sources/run.sh |

## Verification

- Provide a POSIX-compatible `bin/test.sh` that runs the project pytest suite from the application root and exits zero only when every test passes.
- The supplied `sources/run.sh` is the authoritative release conformance grader. Run it as the final verification after all implementation stories are complete; its exit status is the verdict.
- The supplied grader checks command output and HTTP status and JSON response bodies for its defined cases.

## Programmatic Acceptance

=== AC full_release_suite ===
Intent: The supplied grader passes all 35 conformance checks and the project test suite passes.
Suite: full
Requires: executable=sh; scope=test

import subprocess

grader = subprocess.run(
    ["sh", "sources/run.sh"],
    capture_output=True,
    text=True,
)
print(grader.stdout)
print(grader.stderr)
assert grader.returncode == 0

tests = subprocess.run(
    ["sh", "bin/test.sh"],
    capture_output=True,
    text=True,
)
print(tests.stdout)
print(tests.stderr)
assert tests.returncode == 0
=== END AC full_release_suite ===

## User Acceptance

- None.

## Guardrails

- Do not modify, rewrite, regenerate, or substitute files under `sources/`.
- Application code must not read `sources/run.sh` or supplied data files.
- Run the full supplied grader only as terminal release verification.
