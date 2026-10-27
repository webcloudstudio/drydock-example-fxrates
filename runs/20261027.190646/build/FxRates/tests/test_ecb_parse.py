"""Behavior tests for ecb.parse_history: records returned for valid text, RejectedFile for every violation."""

import csv
import io

import pytest

from cli.errors import RejectedFile
from ecb import Rate, parse_history


def _csv(rows: list[list[str]]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    for row in rows:
        writer.writerow(row)
    return buffer.getvalue()


HEADER = ["Date", "USD", "JPY", "HRK", ""]


def test_parse_returns_one_record_per_non_na_value() -> None:
    text = _csv([
        HEADER,
        ["2025-01-03", "1.0299", "161.77", "N/A", ""],
        ["2025-01-02", "1.0321", "N/A", "N/A", ""],
    ])

    records = parse_history(text)

    assert sorted(records) == sorted([
        Rate("2025-01-03", "USD", "1.0299"),
        Rate("2025-01-03", "JPY", "161.77"),
        Rate("2025-01-02", "USD", "1.0321"),
    ])


def test_parse_keeps_the_published_text_including_trailing_zeros() -> None:
    text = _csv([HEADER, ["2025-01-06", "1.10", "162.50", "N/A", ""]])

    records = parse_history(text)

    assert ("2025-01-06", "USD", "1.10") in records
    assert ("2025-01-06", "JPY", "162.50") in records
    assert all(isinstance(record.rate, str) for record in records)


def test_parse_row_of_only_not_available_values_produces_nothing() -> None:
    text = _csv([HEADER, ["2025-01-07", "N/A", "N/A", "N/A", ""]])

    assert parse_history(text) == []


def test_parse_header_only_produces_nothing() -> None:
    assert parse_history(_csv([HEADER])) == []


def test_parse_accepts_a_header_and_rows_without_a_trailing_comma() -> None:
    text = _csv([["Date", "USD"], ["2025-01-03", "1.0299"]])

    assert parse_history(text) == [Rate("2025-01-03", "USD", "1.0299")]


def test_parse_record_unpacks_as_a_three_item_tuple() -> None:
    date, currency, rate = parse_history(_csv([["Date", "USD"], ["2025-01-03", "1.0299"]]))[0]

    assert (date, currency, rate) == ("2025-01-03", "USD", "1.0299")


@pytest.mark.parametrize(
    "rows",
    [
        [["2025-01-03", "1.0299", "161.77", ""], ["2025-01-02", "1.0", ""]],
        [["2025-01-03", "1.0299", "161.77", ""], ["2025-01-02", "1.0", "2.0", "3.0", ""]],
    ],
    ids=["short row", "long row"],
)
def test_parse_rejects_a_row_with_the_wrong_field_count(rows: list[list[str]]) -> None:
    with pytest.raises(RejectedFile):
        parse_history(_csv([["Date", "USD", "JPY", ""], *rows]))


@pytest.mark.parametrize(
    "date",
    ["2025-02-30", "2025-1-2", "20250102", "2025/01/02", "2025-13-01", "abcd-01-02"],
    ids=["impossible", "unpadded", "compact", "slashes", "month 13", "letters"],
)
def test_parse_rejects_an_invalid_date(date: str) -> None:
    with pytest.raises(RejectedFile):
        parse_history(_csv([["Date", "USD"], ["2025-01-03", "1.0"], [date, "2.0"]]))


def test_parse_rejects_a_repeated_date() -> None:
    with pytest.raises(RejectedFile):
        parse_history(_csv([["Date", "USD"], ["2025-01-03", "1.0"], ["2025-01-03", "2.0"]]))


@pytest.mark.parametrize(
    "value",
    ["1.0x", "0", "0.0", "0.00", "-1.5", "1.", ".5", "1,5", "", " 1.0", "1e5"],
    ids=[
        "letters", "zero", "zero point zero", "zero decimals", "negative", "trailing dot",
        "leading dot", "comma decimal", "empty", "leading space", "exponent",
    ],
)
def test_parse_rejects_an_invalid_or_zero_value(value: str) -> None:
    with pytest.raises(RejectedFile):
        parse_history(_csv([["Date", "USD", "JPY"], ["2025-01-03", value, "2.0"]]))


def test_parse_rejects_the_whole_file_when_only_one_row_is_bad() -> None:
    text = _csv([["Date", "USD"], ["2025-01-03", "1.0"], ["2025-01-02", "bad"], ["2025-01-01", "2.0"]])

    with pytest.raises(RejectedFile):
        parse_history(text)


@pytest.mark.parametrize(
    "header",
    [
        ["Day", "USD"],
        ["date", "USD"],
        ["Date", "usd"],
        ["Date", "US"],
        ["Date", "USDX"],
        ["Date", "U5D"],
        ["Date", "USD", "USD"],
    ],
    ids=["first field", "lowercase first field", "lowercase code", "two letters", "four letters",
         "digit in code", "repeated code"],
)
def test_parse_rejects_a_bad_header(header: list[str]) -> None:
    with pytest.raises(RejectedFile):
        parse_history(_csv([header, ["2025-01-03", *(["1.0"] * (len(header) - 1))]]))


def test_parse_rejects_empty_text() -> None:
    with pytest.raises(RejectedFile):
        parse_history("")


def test_parse_rejects_a_blank_row_in_the_body() -> None:
    with pytest.raises(RejectedFile):
        parse_history("Date,USD\n2025-01-03,1.0\n\n2025-01-02,2.0\n")


def test_parse_rejects_an_unterminated_quote_as_rejected_file() -> None:
    with pytest.raises(RejectedFile):
        parse_history('Date,"USD\n2025-01-03,1.0\n\x00')
