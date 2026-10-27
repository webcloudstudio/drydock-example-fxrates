# FEATURE: Offline Test Run

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | `bin/test.sh` runs the pytest suite offline and exits zero only when every test passes. |
| Depends On | FEATURE-CliFoundation.md |
| Provides | bin/test.sh |

## Purpose

A POSIX `sh` script at `bin/test.sh` runs the application's own pytest suite from the application
root, whatever the caller's working directory. No test opens a network connection; the ECB download
is replaced by a stub in `fetch` tests. Each story's builder adds tests beside its code.

## Behavior

- Changes directory to the application root (the parent of `bin/`).
- Activates `.venv` and runs `pytest -q`.
- Exits with pytest's exit status, so it is zero only when every test passes.
- Uses only POSIX `sh` syntax.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC test-script-syntax ===
Intent: bin/test.sh exists and parses as POSIX sh without executing.
Requires: executable=python3; scope=test

import os
import subprocess

script = os.path.abspath("bin/test.sh")
assert os.path.isfile(script)
result = subprocess.run(["sh", "-n", script], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC test-script-syntax ===

=== AC test-script-runs-from-any-directory ===
Intent: Run from an unrelated working directory, the script finds the application root and the suite passes, so its exit status is zero.
Requires: executable=python3; scope=test

import os
import subprocess
import tempfile

script = os.path.abspath("bin/test.sh")
with tempfile.TemporaryDirectory() as elsewhere:
    result = subprocess.run(
        ["sh", script], cwd=elsewhere, capture_output=True, text=True,
        env={**os.environ}, timeout=900,
    )
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC test-script-runs-from-any-directory ===

## User Acceptance

- None.

## Guardrails

- No test opens a network connection; downloads are stubbed.
- The script is POSIX `sh`, with no bash-only syntax.
