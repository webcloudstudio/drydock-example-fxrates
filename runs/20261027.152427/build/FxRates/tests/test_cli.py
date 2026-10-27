"""Dispatcher behavior, exercised in-process through `main` and the `cli_runner` fixture."""

from __future__ import annotations

import sys

import pytest

import cli
from cli import dispatcher
from cli.testing import cli_runner as runner_callable


@pytest.fixture(autouse=True)
def isolated_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Each test registers into its own copy of the registry so commands do not leak."""
    monkeypatch.setattr(dispatcher, "_handlers", dict(dispatcher._handlers))


def test_main_returns_int_for_empty_arguments() -> None:
    code = cli.main([])

    assert isinstance(code, int)
    assert code == dispatcher.USAGE_ERROR


def test_cli_runner_returns_exit_code_and_captured_streams(cli_runner) -> None:
    code, out, err = cli_runner()

    assert code == dispatcher.USAGE_ERROR
    assert isinstance(out, str) and isinstance(err, str)
    assert out == ""


def test_cli_runner_fixture_is_the_testing_callable(cli_runner) -> None:
    assert cli_runner is runner_callable


def test_registered_handler_receives_remaining_arguments() -> None:
    seen: list[list[str]] = []

    def handler(rest: list[str]) -> int:
        seen.append(list(rest))
        return 0

    cli.register_command("probe-args", handler)

    assert cli.main(["probe-args", "alpha", "beta"]) == 0
    assert seen == [["alpha", "beta"]]


def test_handler_without_arguments_receives_empty_list() -> None:
    seen: list[list[str]] = []
    cli.register_command("probe-empty", lambda rest: seen.append(list(rest)) or 0)

    assert cli.main(["probe-empty"]) == 0
    assert seen == [[]]


@pytest.mark.parametrize("exit_code", [0, 1, 3])
def test_handler_exit_code_is_returned_unchanged(exit_code: int) -> None:
    cli.register_command("probe-exit", lambda rest: exit_code)

    assert cli.main(["probe-exit"]) == exit_code


def test_reregistering_a_name_replaces_the_handler() -> None:
    cli.register_command("probe-replace", lambda rest: 1)
    cli.register_command("probe-replace", lambda rest: 5)

    assert cli.main(["probe-replace"]) == 5


def test_unknown_command_returns_usage_error_with_empty_stdout(cli_runner) -> None:
    code, out, _err = cli_runner("no-such-command")

    assert code == dispatcher.USAGE_ERROR
    assert out == ""


def test_handler_output_goes_to_the_captured_streams(cli_runner) -> None:
    def handler(rest: list[str]) -> int:
        print("result", file=sys.stdout)
        print("diagnostic", file=sys.stderr)
        return 0

    cli.register_command("probe-streams", handler)

    code, out, err = cli_runner("probe-streams")

    assert code == 0
    assert out == "result\n"
    assert err == "diagnostic\n"


def test_main_reads_sys_argv_when_argv_is_omitted(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[list[str]] = []
    cli.register_command("probe-argv", lambda rest: seen.append(list(rest)) or 4)
    monkeypatch.setattr(sys, "argv", ["fxrates", "probe-argv", "x"])

    assert cli.main() == 4
    assert seen == [["x"]]
