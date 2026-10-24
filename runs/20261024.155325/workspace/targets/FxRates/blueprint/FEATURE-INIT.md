# FEATURE: Initialize Rates Database

| Field | Value |
|-------|-------|
| Version | 20261024 V1 |
| Description | Defines the command behavior for initializing an empty rates table. |
| Depends On | FEATURE-CLI.md, DATABASE.md |
| Provides | fxrates init |
| Consumes | rates repository operations |

## Purpose

`./fxrates init` drops the rates table if present and recreates it empty. On success it exits 0 and writes nothing to standard output.

## Workflow

1. Resolve the configured database using `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
2. Drop and recreate the rates table through the persistence boundary.
3. Return success without stdout.

## Programmatic Acceptance

=== AC init-success ===
Intent: Initialization succeeds and emits no standard output.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("init")
assert code == 0
assert stdout == ""
=== END AC init-success ===

=== AC init-repeat ===
Intent: Initialization can be run again successfully.

from cli.testing import cli_runner

first = cli_runner("init")
second = cli_runner("init")
assert first[0] == 0
assert second[0] == 0
assert second[1] == ""
=== END AC init-repeat ===

## User Acceptance

- None.

## Guardrails

- Do not access SQLite outside the generated persistence package.
- Do not print a success message.

## Database Interface

- `FEATURE-DATA-009` — write: rates.delete - supplies: `date`, `currency` - returns: `date`, `currency`
