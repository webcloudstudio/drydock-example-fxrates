# FEATURE: Initialize Store

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Resets the rates store through the `fxrates init` command. |
| Depends On  | FEATURE-CLI-Foundation.md, DATABASE.md |
| Provides    | `fxrates init` |
| Consumes    | rates repository operations |

## Purpose

`fxrates init` drops the existing `rates` table and creates it empty through the supported persistence boundary. Success returns exit code `0` and produces no standard output.

## Programmatic Acceptance

=== AC init-exit ===
Intent: Initializing the store succeeds.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("init")
assert code == 0
=== END AC init-exit ===

=== AC init-repeat ===
Intent: Store initialization can be repeated successfully.

from cli.testing import cli_runner

first = cli_runner("init")
second = cli_runner("init")
assert first[0] == 0
assert second[0] == 0
=== END AC init-repeat ===

## User Acceptance

- None.

## Guardrails

- Store initialization uses the shipped persistence boundary.
- Do not print to standard output on successful initialization.
