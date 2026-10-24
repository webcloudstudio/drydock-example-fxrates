# FEATURE: CLI Initialize

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Specifies the command that recreates an empty rates table. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | fxrates init |
| Consumes    | rates persistence operations |

## Purpose

`fxrates init` initializes the configured rates store by dropping the existing rates table, if present, and creating it empty.

## Workflow

1. Resolve the configured store using the project database configuration.
2. Recreate the rates table through the persistence boundary.
3. On success, exit with status `0` and write nothing to standard output.

Usage errors return `2`; operational failures return `1`. A failing command writes no standard output and one diagnostic line to standard error.

## Programmatic Acceptance

=== AC initialize-cli ===
Intent: The init command succeeds and produces no standard output.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("init")
assert code == 0
assert stdout == ""
=== END AC initialize-cli ===

## User Acceptance

- None.

## Guardrails

- Initialization recreates the rates table empty.
- Do not access the database driver outside the shipped persistence library.
