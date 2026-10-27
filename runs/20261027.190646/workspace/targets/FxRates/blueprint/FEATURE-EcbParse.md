# FEATURE: ECB History Parse

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Parse and fully validate an ECB euro reference rate history CSV into rate records without writing anything. |
| Depends On | ARCHITECTURE.md, FEATURE-CliFoundation.md |
| Provides | ecb.parse_history |
| Consumes | cli.main |

## Purpose

`ecb.parse_history(text)` turns the text of an ECB `eurofxref-hist.csv` file into rate records. It performs every validation the source requires and touches no database, so a caller can check a whole file before its first write.

## Interface

- Module `ecb` (package `ecb/`), function `parse_history(text: str) -> list`.
- Each record is a `namedtuple` `Rate(date, currency, rate)` of three strings, so it unpacks as a plain 3-tuple. `rate` is the published text exactly as read.
- Records are returned for every non-`N/A` value. Record order is not part of the contract.
- On any violation the function raises `RejectedFile` (the class owned by the CLI foundation, exit code 3) and returns no records.

## Rules

1. The text is CSV. The header's first field is exactly `Date`, and every other field is a three-letter uppercase currency code. The ECB writes a trailing comma on every line; the resulting empty last field is ignored (one empty trailing field, in the header and in every row).
2. Each row has the same field count as the header and begins with a date in `YYYY-MM-DD` form that is a real calendar date and does not repeat elsewhere in the file.
3. Each value is either `N/A` (no rate; nothing is produced) or matches `[0-9]+(\.[0-9]+)?` and is nonzero (`0`, `0.0`, `0.00` are zero).
4. A row with the wrong field count, an invalid or repeated date, or an invalid value rejects the whole file. Validation covers every row before any record is returned.
5. Rate text is kept exactly as published (`1.10` stays `1.10`). No value is converted to a floating-point number; zero is detected with `decimal.Decimal` or by digits.

## Database Interface

- None — this module is pure parsing and reaches no repository.

## Programmatic Acceptance

=== AC ecb-parse-valid ===
Intent: Every non-N/A value becomes one record carrying the published text unchanged, N/A values and the trailing empty field produce nothing, and trailing zeros survive.
Requires: executable=python3; scope=test

import csv
import io
from ecb import parse_history

header = ["Date", "USD", "JPY", "HRK", ""]
rows = [
    ["2025-01-03", "1.0299", "161.77", "N/A", ""],
    ["2025-01-02", "1.0321", "N/A", "N/A", ""],
    ["2025-01-06", "1.10", "162.5", "N/A", ""],
    ["2025-01-07", "N/A", "N/A", "N/A", ""],
]
buf = io.StringIO()
writer = csv.writer(buf, lineterminator="\n")
writer.writerow(header)
for row in rows:
    writer.writerow(row)

records = parse_history(buf.getvalue())
got = sorted((r[0], r[1], r[2]) for r in records)
expected = sorted(
    (row[0], header[i], row[i])
    for row in rows
    for i in range(1, len(header) - 1)
    if row[i] != "N/A"
)
print(got)
assert got == expected
assert all(isinstance(r[2], str) for r in records)
assert ("2025-01-06", "USD", "1.10") in got
=== END AC ecb-parse-valid ===

=== AC ecb-parse-rejects-bad-rows ===
Intent: A wrong field count, an invalid calendar date, a malformed date, a repeated date, or an invalid or zero value each reject the whole file with RejectedFile even when other rows are valid.
Requires: executable=python3; scope=test

import csv
import io
from ecb import parse_history

header = ["Date", "USD", "JPY", ""]
good = ["2025-01-03", "1.0299", "161.77", ""]


def build(head, rows):
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(head)
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()


cases = {
    "short row": [good, ["2025-01-02", "1.0", ""]],
    "long row": [good, ["2025-01-02", "1.0", "2.0", "3.0", ""]],
    "impossible date": [good, ["2025-02-30", "1.0", "2.0", ""]],
    "unpadded date": [good, ["2025-1-2", "1.0", "2.0", ""]],
    "compact date": [good, ["20250102", "1.0", "2.0", ""]],
    "repeated date": [good, ["2025-01-03", "1.5", "2.5", ""]],
    "letters in value": [good, ["2025-01-02", "1.0x", "2.0", ""]],
    "zero": [good, ["2025-01-02", "0", "2.0", ""]],
    "zero decimals": [good, ["2025-01-02", "1.0", "0.00", ""]],
    "negative": [good, ["2025-01-02", "-1.5", "2.0", ""]],
    "trailing dot": [good, ["2025-01-02", "1.", "2.0", ""]],
    "leading dot": [good, ["2025-01-02", ".5", "2.0", ""]],
    "comma decimal": [good, ["2025-01-02", "1,5", "2.0", ""]],
    "empty value": [good, ["2025-01-02", "", "2.0", ""]],
}

for name, rows in cases.items():
    text = build(header, rows)
    raised = None
    try:
        parse_history(text)
    except Exception as exc:
        raised = exc
    print(name, type(raised).__name__)
    assert raised is not None, name
    assert type(raised).__name__ == "RejectedFile", name
=== END AC ecb-parse-rejects-bad-rows ===

=== AC ecb-parse-rejects-bad-header ===
Intent: A header whose first field is not Date, or that holds a code that is lowercase, two letters, or four letters, rejects the file even when its rows are well formed.
Requires: executable=python3; scope=test

import csv
import io
from ecb import parse_history


def build(head, rows):
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(head)
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()


row = ["2025-01-03", "1.0299", "161.77", ""]
heads = {
    "first field": ["Day", "USD", "JPY", ""],
    "lowercase code": ["Date", "usd", "JPY", ""],
    "two letters": ["Date", "US", "JPY", ""],
    "four letters": ["Date", "USDX", "JPY", ""],
}
for name, head in heads.items():
    raised = None
    try:
        parse_history(build(head, [row]))
    except Exception as exc:
        raised = exc
    print(name, type(raised).__name__)
    assert raised is not None, name
    assert type(raised).__name__ == "RejectedFile", name
=== END AC ecb-parse-rejects-bad-header ===

## User Acceptance

- None.

## Guardrails

- The parser never writes to any store and never opens a database.
- Rates are never converted to floating point; published text is returned as read.
- A rejected file returns no records at all, so no caller can write a partial file.
