# FEATURE: Reject History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Reject invalid ECB history files without changing stored rates. |
| Depends On  | FEATURE-Load-History.md, DATABASE.md |
| Provides    | atomic invalid-file rejection |
| Consumes    | fxrates load, rates repository operations |

## Purpose

A malformed history file must be rejected as a whole. The loader validates every row before its first write, so a valid earlier row in the same file cannot leave partial data behind.

## Behavior

`fxrates load <csv>` returns exit code `3` for a file with a wrong row width, an invalid or repeated date, or an invalid or zero rate. It writes no standard output and emits one diagnostic line to standard error.

A rejected file leaves all previously stored rates unchanged. The loader uses the shared persistence operations declared in `DATABASE.md`.

## Programmatic Acceptance

=== AC reject-invalid-file ===
Intent: The staged malformed history file is rejected with the specified exit status.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("load", "sources/eurofxref-hist_bad.csv")
assert code == 3
=== END AC reject-invalid-file ===

=== AC reject-preserves-existing-rate ===
Intent: Rejecting a file with a valid row before its invalid row leaves an existing rate unchanged.

from cli.testing import cli_runner
from persistence.testing import committed_session

date = "2099-01-06"
currency = "ZZV"
rate = "6.789"

with committed_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

try:
    code, stdout, stderr = cli_runner("load", "sources/eurofxref-hist_bad.csv")
    assert code == 3
    with committed_session() as db:
        row = db.rates.get(date=date, currency=currency)
        assert row is not None
        assert row.rate == rate
finally:
    with committed_session() as db:
        db.rates.delete(date=date, currency=currency)
=== END AC reject-preserves-existing-rate ===

## User Acceptance

- None.

## Guardrails

- Validate the complete file before the first write.
- Rejection must not alter any stored rate.
- Do not access SQLite outside the generated persistence package.
