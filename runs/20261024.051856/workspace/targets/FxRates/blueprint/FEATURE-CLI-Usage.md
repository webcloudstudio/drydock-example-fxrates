# FEATURE: CLI Usage

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines usage errors for unsupported or malformed `fxrates` invocations. |
| Depends On  | FEATURE-CLI-Foundation.md |
| Provides    | CLI usage error behavior |
| Consumes    | ./fxrates entry point |

## Purpose

Return exit code `2` for unknown commands, incorrect argument counts, and a non-integer port value. These usage failures produce no standard output. Write a single diagnostic line to standard error.

## Trigger and behavior

The root `./fxrates` executable dispatches commands. It rejects an unrecognized command, a command with the wrong number of arguments, or `serve --port` followed by a non-integer value with exit code `2`.

## Programmatic Acceptance

=== AC usage-unknown-command ===
Intent: An unknown command returns the usage exit status.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("frobnicate")
assert code == 2
assert stdout == ""
=== END AC usage-unknown-command ===

=== AC usage-wrong-arguments ===
Intent: A command missing its required argument returns the usage exit status.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("load")
assert code == 2
assert stdout == ""
=== END AC usage-wrong-arguments ===

=== AC usage-invalid-port ===
Intent: A non-integer port returns the usage exit status.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("serve", "--port", "notaport")
assert code == 2
assert stdout == ""
=== END AC usage-invalid-port ===

## User Acceptance

- None.

## Guardrails

- Usage failures use exit code `2` and produce no standard output.
