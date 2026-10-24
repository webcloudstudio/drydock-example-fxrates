# FEATURE: Project Test Suite

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Provides the project's pytest suite and POSIX test launcher. |
| Provides    | bin/test.sh, pytest suite |

## Purpose

Provide a POSIX-compatible `bin/test.sh` that runs the project's pytest suite from the application root and exits zero only when all tests pass. The suite covers every CLI command and behavior-changing argument, CSV validity and atomic rejection rules, every API endpoint and response/error behavior, effective-date selection, exact decimal rounding, and `fetch` through a stubbed download. Automated tests must not open a network connection.

## Acceptance Notes

The architecture and feature specifications define the application and its public interfaces. This specification owns the project test suite and its launcher, not product runtime behavior.

## Programmatic Acceptance

=== AC test-launcher ===
Intent: The project test launcher completes successfully after the suite is provided.

import subprocess

result = subprocess.run(
    ["sh", "bin/test.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC test-launcher ===

## User Acceptance

- None.

## Guardrails

- Keep the test suite under the project test directory and runnable from the application root.
- Stub fetch downloads; the tests must never use the network.
