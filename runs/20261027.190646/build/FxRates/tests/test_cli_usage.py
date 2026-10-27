"""Behavior tests for cli.usage.parse and for usage errors reaching the exit code through main."""

from pathlib import Path

import pytest

from cli.errors import UsageError
from cli.usage import DEFAULT_PORT, parse


def test_parse_init_hands_over_no_arguments() -> None:
    assert parse(["init"]) == ("init", [])


def test_parse_fetch_hands_over_no_arguments() -> None:
    assert parse(["fetch"]) == ("fetch", [])


def test_parse_load_hands_over_its_single_path() -> None:
    assert parse(["load", "rates.csv"]) == ("load", ["rates.csv"])


def test_parse_serve_defaults_the_port_to_an_integer() -> None:
    assert parse(["serve"]) == ("serve", [DEFAULT_PORT])
    assert DEFAULT_PORT == 8000


def test_parse_serve_converts_the_port_text_to_an_integer() -> None:
    _, args = parse(["serve", "--port", "9123"])

    assert args == [9123]
    assert isinstance(args[0], int)


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["frobnicate"],
        ["init", "extra"],
        ["fetch", "extra"],
        ["load"],
        ["load", "a.csv", "b.csv"],
        ["load", "--force", "a.csv"],
        ["serve", "--port"],
        ["serve", "--port", "notaport"],
        ["serve", "--port", "1.5"],
        ["serve", "--port", "9", "extra"],
        ["serve", "--host", "127.0.0.1"],
    ],
)
def test_parse_raises_usage_error_for_a_malformed_invocation(argv: list[str]) -> None:
    with pytest.raises(UsageError):
        parse(argv)


@pytest.mark.parametrize("argv", [[], ["frobnicate"], ["load"], ["serve", "--port", "x1"]])
def test_usage_error_declares_exit_code_two(argv: list[str]) -> None:
    with pytest.raises(UsageError) as info:
        parse(argv)

    assert info.value.exit_code == 2


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["frobnicate"],
        ["load"],
        ["load", "a.csv", "b.csv"],
        ["init", "extra"],
        ["fetch", "extra"],
        ["serve", "--port", "notaport"],
        ["serve", "--port"],
    ],
)
def test_usage_error_from_the_command_line_exits_two_with_empty_stdout(cli_runner, argv: list[str]) -> None:
    code, out, err = cli_runner(*argv)

    assert code == 2
    assert out == ""
    assert len(err.strip().splitlines()) == 1


def test_usage_error_does_not_create_the_store(cli_runner, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    store = tmp_path / "never-created.db"
    monkeypatch.setenv("DATABASE_URL", str(store))
    monkeypatch.delenv("DATABASE_PATH", raising=False)

    code, _, _ = cli_runner("load")

    assert code == 2
    assert not store.exists()
