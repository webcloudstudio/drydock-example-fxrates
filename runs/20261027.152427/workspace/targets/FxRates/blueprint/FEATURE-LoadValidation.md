# FEATURE: Load Validation

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Validate a whole ECB history file before any write and return the non-N/A rates as published text. |
| Depends On | FEATURE-InitCommand.md |
| Provides | fxrates_app.ecb.parse_history |

## Purpose

`fxrates_app.ecb.parse_history(text)` checks an entire ECB history file and returns
`(date, currency, rate_text)` for every non-N/A value, or raises `RejectedFile`. It performs no
database access. The load command (FEATURE-LoadStore.md) maps `RejectedFile` to exit 3.

## Rules

1. The header's first field is `Date`; every other field is a three-letter uppercase currency code.
   The ECB writes a trailing comma on each line; the resulting empty last field is ignored.
2. Each row has exactly as many fields as the header, and begins with a date `YYYY-MM-DD` that is a
   real calendar date and is not repeated within the file.
3. A value is `N/A` (no rate, nothing returned) or matches `[0-9]+(\.[0-9]+)?` and is nonzero.
4. The whole file is checked before the function returns; any violation raises `RejectedFile`, a
   subclass of `Exception`.
5. Rates are returned as the published text, never as a number.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC parse-valid-file ===
Intent: A valid file yields exactly its non-N/A cells as (date, currency, text) with the published text unchanged, ignoring the trailing comma.
Requires: executable=python3; scope=test

import csv
import io
from fxrates_app.ecb import parse_history

def build(header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header + [""])
    for r in rows:
        w.writerow(r + [""])
    return buf.getvalue()

header = ["Date", "ZZA", "ZZB", "ZZC"]
rows = [
    ["1900-01-03", "1.50", "N/A", "160.0"],
    ["1900-01-02", "0.943", "2", "N/A"],
]
result = parse_history(build(header, rows))
expected = []
for r in rows:
    for code, v in zip(header[1:], r[1:]):
        if v != "N/A":
            expected.append((r[0], code, v))
assert sorted(tuple(x) for x in result) == sorted(expected)
=== END AC parse-valid-file ===

=== AC parse-only-na ===
Intent: A file whose values are all N/A is valid and yields no rates.
Requires: executable=python3; scope=test

import csv
import io
from fxrates_app.ecb import parse_history

buf = io.StringIO()
w = csv.writer(buf, lineterminator="\n")
w.writerow(["Date", "ZZA", "ZZB", ""])
w.writerow(["1900-01-02", "N/A", "N/A", ""])
assert list(parse_history(buf.getvalue())) == []
=== END AC parse-only-na ===

=== AC parse-rejects-structure ===
Intent: A wrong first header field, a malformed currency code, or a row with the wrong field count rejects the file.
Requires: executable=python3; scope=test

import csv
import io
from fxrates_app.ecb import parse_history, RejectedFile

assert issubclass(RejectedFile, Exception)

def build(header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header + [""])
    for r in rows:
        w.writerow(r + [""])
    return buf.getvalue()

def rejected(text):
    try:
        parse_history(text)
    except RejectedFile:
        return True
    return False

good_row = ["1900-01-02", "1.5", "2.5"]
cases = {
    "bad first field": build(["Day", "ZZA", "ZZB"], [good_row]),
    "lowercase code": build(["Date", "zza", "ZZB"], [good_row]),
    "four letter code": build(["Date", "ZZAA", "ZZB"], [good_row]),
    "short row": build(["Date", "ZZA", "ZZB"], [["1900-01-02", "1.5"]]),
    "long row": build(["Date", "ZZA", "ZZB"], [["1900-01-02", "1.5", "2.5", "3.5"]]),
}
for name, text in cases.items():
    assert rejected(text), name
=== END AC parse-rejects-structure ===

=== AC parse-rejects-dates ===
Intent: A malformed, impossible, or repeated date rejects the whole file even when other rows are valid.
Requires: executable=python3; scope=test

import csv
import io
from fxrates_app.ecb import parse_history, RejectedFile

def build(header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header + [""])
    for r in rows:
        w.writerow(r + [""])
    return buf.getvalue()

def rejected(text):
    try:
        parse_history(text)
    except RejectedFile:
        return True
    return False

header = ["Date", "ZZA"]
valid = ["1900-01-02", "1.5"]
cases = {
    "unpadded": [valid, ["1900-1-3", "1.5"]],
    "not a calendar date": [valid, ["1900-02-30", "1.5"]],
    "month thirteen": [valid, ["1900-13-01", "1.5"]],
    "repeated": [valid, ["1900-01-03", "1.6"], ["1900-01-03", "1.7"]],
    "text": [valid, ["yesterday", "1.5"]],
}
for name, rows in cases.items():
    assert rejected(build(header, rows)), name
=== END AC parse-rejects-dates ===

=== AC parse-rejects-values ===
Intent: Any value that is neither N/A nor a nonzero decimal matching the ECB pattern rejects the file, even when it is on a later row.
Requires: executable=python3; scope=test

import csv
import io
from fxrates_app.ecb import parse_history, RejectedFile

def build(header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header + [""])
    for r in rows:
        w.writerow(r + [""])
    return buf.getvalue()

def rejected(text):
    try:
        parse_history(text)
    except RejectedFile:
        return True
    return False

header = ["Date", "ZZA", "ZZB"]
first = ["1900-01-03", "1.5", "2.5"]
for bad in ["1.0x", "0", "0.00", "-1", ".5", "1.", "", "abc", "1e3"]:
    text = build(header, [first, ["1900-01-02", bad, "2.5"]])
    assert rejected(text), bad
=== END AC parse-rejects-values ===

## User Acceptance

- None.

## Guardrails

- The whole file is checked before any result is returned; callers never see a partial parse.
- Rates are never converted to a float; the published text is preserved.
- The parser performs no database access and reads no file.
