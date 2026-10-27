"""ECB history file validation: one pure function checks a whole file before any write.

`parse_history` reads the text of an ECB euro reference rate history file and returns every
non-N/A value as (date, currency, rate_text). It performs no database access and reads no file.
Rates keep their published text; they are never converted to a number.
"""

from __future__ import annotations

import csv
import datetime
import io
import re
from decimal import Decimal

FIRST_HEADER_FIELD = "Date"
NOT_AVAILABLE = "N/A"

_DATE_PATTERN = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
_CURRENCY_PATTERN = re.compile(r"[A-Z]{3}")
_RATE_PATTERN = re.compile(r"[0-9]+(\.[0-9]+)?")


class RejectedFile(Exception):
    """Raised when an ECB history file violates the format; no rate from it may be written."""


def parse_history(text: str) -> list[tuple[str, str, str]]:
    """Validate the whole file and return (date, currency, rate_text) for every non-N/A value.

    Raises RejectedFile on the first violation found anywhere in the file.
    """
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        raise RejectedFile("file has no header")

    header = _drop_trailing_comma(rows[0])
    if not header or header[0] != FIRST_HEADER_FIELD:
        raise RejectedFile("header must begin with Date")
    currencies = header[1:]
    for code in currencies:
        if not _CURRENCY_PATTERN.fullmatch(code):
            raise RejectedFile(f"malformed currency code in header: {code!r}")
    if len(set(currencies)) != len(currencies):
        raise RejectedFile("currency code repeated in header")

    rates: list[tuple[str, str, str]] = []
    seen_dates: set[str] = set()
    for line_number, raw in enumerate(rows[1:], start=2):
        fields = _drop_trailing_comma(raw)
        if len(fields) != len(header):
            raise RejectedFile(f"line {line_number} has {len(fields)} fields, expected {len(header)}")

        date_text = fields[0]
        _check_date(date_text, line_number)
        if date_text in seen_dates:
            raise RejectedFile(f"line {line_number} repeats date {date_text}")
        seen_dates.add(date_text)

        for code, value in zip(currencies, fields[1:]):
            if value == NOT_AVAILABLE:
                continue
            _check_rate(value, line_number)
            rates.append((date_text, code, value))

    return rates


def _drop_trailing_comma(fields: list[str]) -> list[str]:
    """The ECB writes a trailing comma on each line; the resulting empty last field is ignored."""
    if fields and fields[-1] == "":
        return fields[:-1]
    return fields


def _check_date(text: str, line_number: int) -> None:
    if not _DATE_PATTERN.fullmatch(text):
        raise RejectedFile(f"line {line_number} has a malformed date: {text!r}")
    try:
        datetime.date.fromisoformat(text)
    except ValueError as error:
        raise RejectedFile(f"line {line_number} has an impossible date: {text!r}") from error


def _check_rate(text: str, line_number: int) -> None:
    if not _RATE_PATTERN.fullmatch(text):
        raise RejectedFile(f"line {line_number} has a malformed rate: {text!r}")
    if Decimal(text) == 0:
        raise RejectedFile(f"line {line_number} has a zero rate: {text!r}")
