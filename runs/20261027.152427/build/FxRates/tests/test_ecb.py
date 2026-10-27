"""ECB history validation: parse_history checks a whole file and returns published rate text.

The function is pure, so each test builds a file in memory, parses it, and compares the returned
tuples (or the RejectedFile signal) with the expected values.
"""

from __future__ import annotations

import csv
import io

import pytest

from fxrates_app.ecb import RejectedFile, parse_history


def build(header: list[str], rows: list[list[str]]) -> str:
    """Write a file the way the ECB does: every line ends with a trailing comma."""
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(header + [""])
    for row in rows:
        writer.writerow(row + [""])
    return buf.getvalue()


def rejected(text: str) -> bool:
    try:
        parse_history(text)
    except RejectedFile:
        return True
    return False


def test_rejected_file_is_an_exception() -> None:
    assert issubclass(RejectedFile, Exception)


def test_valid_file_yields_every_non_na_cell_with_published_text() -> None:
    header = ["Date", "ZZA", "ZZB", "ZZC"]
    rows = [
        ["1900-01-03", "1.50", "N/A", "160.0"],
        ["1900-01-02", "0.943", "2", "N/A"],
    ]

    result = parse_history(build(header, rows))

    assert sorted(result) == sorted(
        [
            ("1900-01-03", "ZZA", "1.50"),
            ("1900-01-03", "ZZC", "160.0"),
            ("1900-01-02", "ZZA", "0.943"),
            ("1900-01-02", "ZZB", "2"),
        ]
    )


def test_trailing_comma_is_not_a_currency_or_a_value() -> None:
    result = parse_history(build(["Date", "ZZA"], [["1900-01-02", "1.5"]]))

    assert result == [("1900-01-02", "ZZA", "1.5")]


def test_file_of_only_na_values_is_valid_and_yields_nothing() -> None:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["Date", "ZZA", "ZZB", ""])
    writer.writerow(["1900-01-02", "N/A", "N/A", ""])

    assert list(parse_history(buf.getvalue())) == []


def test_header_only_file_yields_nothing() -> None:
    assert list(parse_history(build(["Date", "ZZA"], []))) == []


def test_empty_text_is_rejected_for_missing_header() -> None:
    assert rejected("")


@pytest.mark.parametrize(
    "name, header",
    [
        ("bad first field", ["Day", "ZZA", "ZZB"]),
        ("lowercase code", ["Date", "zza", "ZZB"]),
        ("four letter code", ["Date", "ZZAA", "ZZB"]),
        ("two letter code", ["Date", "ZZ", "ZZB"]),
        ("repeated code", ["Date", "ZZA", "ZZA"]),
    ],
)
def test_bad_header_rejects_the_file(name: str, header: list[str]) -> None:
    assert rejected(build(header, [["1900-01-02", "1.5", "2.5"]])), name


@pytest.mark.parametrize(
    "name, row",
    [
        ("short row", ["1900-01-02", "1.5"]),
        ("long row", ["1900-01-02", "1.5", "2.5", "3.5"]),
    ],
)
def test_row_with_wrong_field_count_rejects_the_file(name: str, row: list[str]) -> None:
    assert rejected(build(["Date", "ZZA", "ZZB"], [row])), name


def test_blank_line_in_the_middle_rejects_the_file() -> None:
    text = "Date,ZZA,\n1900-01-03,1.5,\n\n1900-01-02,2.5,\n"

    assert rejected(text)


@pytest.mark.parametrize(
    "name, date",
    [
        ("unpadded", "1900-1-3"),
        ("not a calendar date", "1900-02-30"),
        ("month thirteen", "1900-13-01"),
        ("text", "yesterday"),
        ("compact form", "19000102"),
    ],
)
def test_malformed_or_impossible_date_rejects_the_whole_file(name: str, date: str) -> None:
    header = ["Date", "ZZA"]
    rows = [["1900-01-02", "1.5"], [date, "1.5"]]

    assert rejected(build(header, rows)), name


def test_repeated_date_rejects_the_whole_file() -> None:
    header = ["Date", "ZZA"]
    rows = [["1900-01-02", "1.5"], ["1900-01-03", "1.6"], ["1900-01-03", "1.7"]]

    assert rejected(build(header, rows))


def test_leap_day_is_a_real_calendar_date() -> None:
    result = parse_history(build(["Date", "ZZA"], [["2024-02-29", "1.5"]]))

    assert result == [("2024-02-29", "ZZA", "1.5")]


@pytest.mark.parametrize("bad", ["1.0x", "0", "0.00", "-1", ".5", "1.", "", "abc", "1e3"])
def test_invalid_value_rejects_even_when_on_a_later_row(bad: str) -> None:
    header = ["Date", "ZZA", "ZZB"]
    first = ["1900-01-03", "1.5", "2.5"]

    assert rejected(build(header, [first, ["1900-01-02", bad, "2.5"]])), bad


def test_zero_in_a_later_column_rejects_the_file() -> None:
    assert rejected(build(["Date", "ZZA", "ZZB"], [["1900-01-02", "1.5", "0.000"]]))


def test_rate_text_is_returned_unchanged_not_as_a_number() -> None:
    result = parse_history(build(["Date", "ZZA"], [["1900-01-02", "1.50000"]]))

    assert result == [("1900-01-02", "ZZA", "1.50000")]
    assert isinstance(result[0][2], str)


def test_parsing_twice_gives_the_same_result() -> None:
    text = build(["Date", "ZZA", "ZZB"], [["1900-01-02", "1.5", "N/A"]])

    assert parse_history(text) == parse_history(text)
