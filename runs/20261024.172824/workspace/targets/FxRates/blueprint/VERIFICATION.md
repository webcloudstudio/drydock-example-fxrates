# FEATURE: End-to-End Verification

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Runs the supplied end-to-end grader against the completed FxRates application. |
| Depends On  | FEATURE-Initialize.md, FEATURE-Load.md, FEATURE-Fetch.md, FEATURE-CLI-Errors.md, FEATURE-Serve.md, FEATURE-Health-Stats.md, FEATURE-Currencies.md, FEATURE-Rates.md, FEATURE-Convert.md, FEATURE-History.md |
| Provides    | supplied end-to-end conformance grader |

## Scope

The supplied `sources/run.sh` is the authoritative, externally authored conformance grader. It exercises the executable, command output and exit codes, server startup, HTTP status codes and JSON bodies, and visibility of data loaded while the server is running. It is staged with its CSV inputs and must remain unchanged. Run it only after the implementation stories have completed.

## Programmatic Acceptance

=== AC fxrates-full-conformance ===
Intent: The supplied end-to-end grader passes all of its checks.
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
=== END AC fxrates-full-conformance ===

## User Acceptance

- None.

## Guardrails

- Do not modify, rewrite, regenerate, or substitute any file under `sources/`.
- Keep the supplied grader as the terminal full-suite gate; do not run it in intermediate stories.
- Application code must not read the grader or embed its known answers.
