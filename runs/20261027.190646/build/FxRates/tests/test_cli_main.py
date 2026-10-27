"""Behavior tests for cli.main and the cli_runner fixture, using registered in-memory command modules."""

import sys
import types
from collections.abc import Callable
from pathlib import Path

import pytest

import cli.commands
from cli import main
from cli.errors import OperationalError
from cli.testing import cli_runner as direct_cli_runner


def _register_command(monkeypatch: pytest.MonkeyPatch, name: str, run: Callable[[list[str]], int]) -> None:
    module = types.ModuleType(f"cli.commands.{name}")
    module.run = run  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, f"cli.commands.{name}", module)


def test_main_returns_the_exit_code_of_the_named_command(monkeypatch: pytest.MonkeyPatch) -> None:
    _register_command(monkeypatch, "probe", lambda args: 0)

    assert main(["probe"]) == 0


def test_main_passes_the_remaining_arguments_to_the_command(monkeypatch: pytest.MonkeyPatch) -> None:
    received: list[list[str]] = []

    def run(args: list[str]) -> int:
        received.append(args)
        return 0

    _register_command(monkeypatch, "probe", run)

    main(["probe", "alpha", "--beta"])

    assert received == [["alpha", "--beta"]]


def test_main_returns_a_nonzero_command_result_unchanged(monkeypatch: pytest.MonkeyPatch) -> None:
    _register_command(monkeypatch, "probe", lambda args: 3)

    assert main(["probe"]) == 3


def test_main_maps_an_operational_failure_to_exit_code_one(monkeypatch: pytest.MonkeyPatch) -> None:
    def run(args: list[str]) -> int:
        raise OperationalError("probe could not finish")

    _register_command(monkeypatch, "probe", run)

    assert main(["probe"]) == 1


def test_main_defaults_to_the_process_arguments(monkeypatch: pytest.MonkeyPatch) -> None:
    received: list[list[str]] = []

    def run(args: list[str]) -> int:
        received.append(args)
        return 0

    _register_command(monkeypatch, "probe", run)
    monkeypatch.setattr(sys, "argv", ["fxrates", "probe", "from-argv"])

    assert main() == 0
    assert received == [["from-argv"]]


def test_main_with_no_command_returns_usage_exit_code() -> None:
    assert main([]) == 2


def test_main_with_an_unknown_command_returns_usage_exit_code() -> None:
    assert main(["zzprobe-unknown-command"]) == 2


def test_unknown_command_writes_nothing_to_stdout(cli_runner) -> None:
    _, out, _ = cli_runner("zzprobe-unknown-command")

    assert out == ""


def test_unknown_command_writes_one_stderr_line(cli_runner) -> None:
    _, _, err = cli_runner("zzprobe-unknown-command")

    assert len(err.splitlines()) == 1


def test_cli_runner_returns_the_exit_code_stdout_and_stderr_of_a_command(monkeypatch: pytest.MonkeyPatch) -> None:
    def run(args: list[str]) -> int:
        print("hello")
        return 0

    _register_command(monkeypatch, "probe", run)

    code, out, err = direct_cli_runner("probe")

    assert (code, out, err) == (0, "hello\n", "")


def test_cli_runner_returns_a_three_part_tuple(cli_runner) -> None:
    result = cli_runner("zzprobe-unknown-command")

    assert isinstance(result, tuple)
    assert len(result) == 3
    assert isinstance(result[0], int)
    assert isinstance(result[1], str)
    assert isinstance(result[2], str)


def test_cli_runner_fixture_is_the_runner_function(cli_runner) -> None:
    assert cli_runner is direct_cli_runner


def test_command_import_failure_inside_a_command_propagates(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # A command module that exists but imports a missing dependency is a broken command, not an unknown one.
    (tmp_path / "broken.py").write_text("import zz_no_such_module_for_probe\n", encoding="utf-8")
    monkeypatch.setattr(cli.commands, "__path__", [str(tmp_path)])

    with pytest.raises(ModuleNotFoundError):
        main(["broken"])
