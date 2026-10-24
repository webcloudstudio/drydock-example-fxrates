# FEATURE: CLI Fetch

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Specifies downloading and loading the ECB reference-rate archive. |
| Depends On  | ARCHITECTURE.md, FEATURE-CLI-Load.md |
| Provides    | fxrates fetch |
| Consumes    | fxrates load |

## Purpose

`fxrates fetch` downloads `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip`, extracts `eurofxref-hist.csv`, and applies the same full-file validation, atomicity, replacement, and count reporting as `fxrates load`.

A failed download is an operational failure: exit `1`, no stdout, and one diagnostic line on stderr.

## Programmatic Acceptance

=== AC fetch-help-surface ===
Intent: The fetch command is callable through the CLI interface.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("fetch")
assert code in (0, 1, 2)
=== END AC fetch-help-surface ===

## User Acceptance

- None.

## Guardrails

- Automated fetch tests must stub the download and must not use the network.
- Feed extracted CSV through the same loader used by `fxrates load`.
