# FEATURE: Store Initialization

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Defines the CLI behavior for resetting the rates store. |
| Depends On  | FEATURE-CLI.md, DATABASE.md |
| Provides    | `./fxrates init` |
| Consumes    | `./fxrates`, rates repository operations |

## Purpose

`fxrates init` resets the rates store to an empty state. It takes no arguments, prints nothing on success, and uses the persistence boundary.

## Programmatic Acceptance

=== AC init-clears-store ===
Intent: The init command succeeds and leaves the rates repository empty.

from cli.testing import cli_runner
from persistence.testing import db_session

with db_session() as db:
    db.rates.upsert(date="2099-06-01", currency="QAF", rate="6.1")

code, stdout, stderr = cli_runner("init")
assert code == 0
assert stdout == ""

with db_session() as db:
    rows = db.rates.list()
    assert rows == []
=== END AC init-clears-store ===

=== AC init-rejects-extra-arguments ===
Intent: The init command rejects an unexpected argument with the usage exit status.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("init", "extra")
assert code == 2
=== END AC init-rejects-extra-arguments ===

## User Acceptance

- None.

## Guardrails

- Reset the rates table through the persistence boundary.
- Keep diagnostics on standard error.
