# FEATURE: CLI Init

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Initializes the rates store through the command line. |
| Depends On  | DATABASE.md, ARCHITECTURE.md |
| Provides    | fxrates init |
| Consumes    | rates repository operations |

## Purpose

The `fxrates init` command initializes the rates database and leaves it empty. It prints nothing on success.

## Workflow

1. Invoke `./fxrates init`.
2. Reinitialize the configured store through the persistence boundary.
3. Ensure the rates table has no rows after initialization.

## Database Interface


- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC cli-init-empty ===
Intent: Initialization succeeds silently and leaves no rate rows in the configured store.

from cli.testing import cli_runner
from persistence.testing import db_session

code, out, err = cli_runner("init")
assert code == 0
assert out == ""
with db_session() as db:
    assert db.rates.list_all() == []
=== END AC cli-init-empty ===

=== AC cli-init-repeat ===
Intent: Repeating initialization succeeds and leaves the rates store empty.

from cli.testing import cli_runner
from persistence.testing import db_session

first_code, _, _ = cli_runner("init")
second_code, out, _ = cli_runner("init")
assert first_code == 0
assert second_code == 0
assert out == ""
with db_session() as db:
    assert db.rates.list_all() == []
=== END AC cli-init-repeat ===

## User Acceptance

- None.

## Guardrails

- Use the configured database location.
- Do not print success output.
