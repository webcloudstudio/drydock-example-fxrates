"""Usage validation: malformed invocations exit 2 with empty stdout and one stderr line.

Exercised in-process through `cli_runner` and `cli.usage.validate`; no process is spawned.
"""

from __future__ import annotations

import pytest

from cli import dispatcher
from cli.usage import UsageError, validate

MALFORMED = [
    [],
    ["frobnicate"],
    ["load"],
    ["load", "a.csv", "b.csv"],
    ["init", "extra"],
    ["fetch", "extra"],
    ["serve", "--port", "notaport"],
    ["serve", "--port"],
    ["serve", "--port", "0"],
    ["serve", "--port", "65536"],
    ["serve", "--port", "-1"],
    ["serve", "--port", "1.5"],
    ["serve", "extra"],
    ["serve", "--port", "8000", "extra"],
]

VALID = [
    ["serve"],
    ["serve", "--port", "1"],
    ["serve", "--port", "65535"],
    ["serve", "--port", "8000"],
    ["init"],
    ["load", "x.csv"],
    ["fetch"],
]


@pytest.fixture(autouse=True)
def isolated_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Each test registers into its own copy of the registry so commands do not leak."""
    monkeypatch.setattr(dispatcher, "_handlers", dict(dispatcher._handlers))


@pytest.mark.parametrize("argv", MALFORMED, ids=lambda argv: " ".join(argv) or "no-command")
def test_malformed_invocation_exits_2_with_empty_stdout(cli_runner, argv: list[str]) -> None:
    code, out, err = cli_runner(*argv)

    assert code == 2
    assert out == ""
    assert len(err.strip().splitlines()) == 1


@pytest.mark.parametrize("argv", VALID, ids=lambda argv: " ".join(argv))
def test_valid_invocation_passes_validation(argv: list[str]) -> None:
    validate(argv)


@pytest.mark.parametrize("argv", MALFORMED, ids=lambda argv: " ".join(argv) or "no-command")
def test_validate_raises_usage_error_for_malformed_invocation(argv: list[str]) -> None:
    with pytest.raises(UsageError):
        validate(argv)


@pytest.mark.parametrize("port", ["1", "65535"])
def test_port_boundaries_are_accepted(port: str) -> None:
    validate(["serve", "--port", port])


@pytest.mark.parametrize("port", ["0", "65536", "-1", "notaport", "", "+80"])
def test_out_of_range_or_non_integer_port_is_rejected(port: str) -> None:
    with pytest.raises(UsageError):
        validate(["serve", "--port", port])


@pytest.mark.parametrize("argv", [["init", "--help"], ["load", "--help"], ["fetch", "--help"], ["serve", "--help"]])
def test_lone_help_after_known_command_passes_through(argv: list[str]) -> None:
    validate(argv)


def test_registered_command_outside_table_is_not_arity_checked() -> None:
    validate(["probe", "a", "b", "c"], registered=["probe"])


def test_command_outside_table_and_registry_is_rejected() -> None:
    with pytest.raises(UsageError):
        validate(["probe"], registered=[])


def test_empty_argv_is_rejected() -> None:
    with pytest.raises(UsageError):
        validate([])


def test_usage_error_is_raised_before_handler_runs(cli_runner) -> None:
    calls: list[list[str]] = []
    dispatcher.register_command("init", lambda rest: calls.append(list(rest)) or 0)

    code, out, err = cli_runner("init", "extra")

    assert code == 2
    assert out == ""
    assert len(err.strip().splitlines()) == 1
    assert calls == []


def test_registered_handler_still_receives_valid_arguments(cli_runner) -> None:
    calls: list[list[str]] = []
    dispatcher.register_command("serve", lambda rest: calls.append(list(rest)) or 0)

    code, _out, _err = cli_runner("serve", "--port", "8000")

    assert code == 0
    assert calls == [["--port", "8000"]]
