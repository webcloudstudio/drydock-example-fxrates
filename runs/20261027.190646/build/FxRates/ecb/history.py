"""Parse and fully validate an ECB euro reference rate history CSV.

The parser touches no store. A file that breaks any rule raises RejectedFile before any record is
returned, so a caller can never write part of a refused file. Rate text is kept as published;
decimal.Decimal is used only to detect a zero value.
"""

from __future__ import annotations

import csv
import datetime
import io
import re
from decimal import Decimal
from typing import NamedTuple

from cli.errors import RejectedFile

NOT_AVAILABLE = "N/A"
_HEADER_DATE = "Date"
_CURRENCY = re.compile(r"[A-Z]{3}")
_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
_RATE = re.compile(r"[0-9]+(\.[0-9]+)?")


class Rate(NamedTuple):
    """One published rate: its date, its currency code and its value as the published text."""

    date: str
    currency: str
    rate: str


def parse_history(text: str) -> list[Rate]:
    """Return one Rate per non-N/A value in the ECB history text; raise RejectedFile on any violation."""
    rows = _read_rows(text)
    if not rows:
        raise RejectedFile("the file is empty; it has no header row")
    header = _without_trailing_empty(rows[0])
    if not header or header[0] != _HEADER_DATE:
        raise RejectedFile("the header row must begin with Date")
    currencies = header[1:]
    for code in currencies:
        if not _CURRENCY.fullmatch(code):
            raise RejectedFile(f"header field {code!r} is not a three-letter uppercase currency code")
    if len(set(currencies)) != len(currencies):
        raise RejectedFile("the header row repeats a currency code")

    records: list[Rate] = []
    seen_dates: set[str] = set()
    for number, raw in enumerate(rows[1:], start=2):
        fields = _without_trailing_empty(raw)
        if len(fields) != len(header):
            raise RejectedFile(f"row {number} has {len(fields)} fields; the header has {len(header)}")
        date = fields[0]
        if not _is_calendar_date(date):
            raise RejectedFile(f"row {number} has an invalid date {date!r}")
        if date in seen_dates:
            raise RejectedFile(f"row {number} repeats the date {date}")
        seen_dates.add(date)
        for code, value in zip(currencies, fields[1:], strict=True):
            if value == NOT_AVAILABLE:
                continue
            if not _is_positive_rate(value):
                raise RejectedFile(f"row {number} has an invalid value {value!r} for {code}")
            records.append(Rate(date=date, currency=code, rate=value))
    return records


def _read_rows(text: str) -> list[list[str]]:
    try:
        return list(csv.reader(io.StringIO(text)))
    except csv.Error as exc:
        raise RejectedFile(f"the file is not readable CSV: {exc}") from exc


def _without_trailing_empty(fields: list[str]) -> list[str]:
    """The ECB writes a trailing comma on every line; drop that one empty field when present."""
    if fields and fields[-1] == "":
        return fields[:-1]
    return fields


def _is_calendar_date(text: str) -> bool:
    if not _DATE.fullmatch(text):
        return False
    try:
        datetime.date.fromisoformat(text)
    except ValueError:
        return False
    return True


def _is_positive_rate(text: str) -> bool:
    return bool(_RATE.fullmatch(text)) and Decimal(text) != 0
