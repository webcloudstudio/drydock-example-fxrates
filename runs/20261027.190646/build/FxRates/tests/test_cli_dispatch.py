"""Behavior tests for cli.dispatch: handler results, error-to-exit-code mapping and command resolution."""

import sys
import types
from collections.abc import Callable

import pytest

from cli.dispatch import dispatch, execute, resolve
from cli.errors import OperationalError, RejectedFile, UsageError


def _register_command(monkeypatch: pytest.MonkeyPatch, name: str, run: Callable[[list[str]], int]) -> None:
    """Make cli.commands.<name> importable as a module whose run() is the given callable."""
    module = types.ModuleType(f"cli.commands.{name}")
    module.run = run  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, f"cli.commands.{name}", module)


def test_execute_returns_the_handler_result() -> None:
    assert execute(lambda args: 0, []) == 0


def test_execute_returns_a_nonzero_handler_result_unchanged() -> None:
    assert execute(lambda args: 5, []) == 5


def test_execute_passes_the_arguments_to_the_handler() -> None:
    received: list[list[str]] = []

    def handler(args: list[str]) -> int:
        received.append(args)
        return 0

    execute(handler, ["alpha", "--beta"])

    assert received == [["alpha", "--beta"]]


@pytest.mark.parametrize(
    ("error_class", "expected_code"),
    [(OperationalError, 1), (UsageError, 2), (RejectedFile, 3)],
)
def test_execute_maps_each_expected_error_to_its_exit_code(
    error_class: type[Exception], expected_code: int
) -> None:
    def handler(args: list[str]) -> int:
        raise error_class("probe failure")

    assert execute(handler, []) == expected_code


@pytest.mark.parametrize("error_class", [OperationalError, UsageError, RejectedFile])
def test_execute_writes_nothing_to_stdout_on_an_expected_error(
    error_class: type[Exception], capsys: pytest.CaptureFixture[str]
) -> None:
    def handler(args: list[str]) -> int:
        raise error_class("probe failure")

    execute(handler, [])

    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("error_class", [OperationalError, UsageError, RejectedFile])
def test_execute_writes_exactly_one_diagnostic_line_on_an_expected_error(
    error_class: type[Exception], capsys: pytest.CaptureFixture[str]
) -> None:
    def handler(args: list[str]) -> int:
        raise error_class("probe failure")

    execute(handler, [])

    assert len(capsys.readouterr().err.splitlines()) == 1


def test_execute_keeps_a_multiline_message_to_one_stderr_line(capsys: pytest.CaptureFixture[str]) -> None:
    def handler(args: list[str]) -> int:
        raise OperationalError("first part\nsecond part")

    code = execute(handler, [])

    assert code == 1
    assert len(capsys.readouterr().err.splitlines()) == 1


def test_execute_lets_an_unexpected_exception_propagate() -> None:
    def handler(args: list[str]) -> int:
        raise ValueError("not an expected failure")

    with pytest.raises(ValueError):
        execute(handler, [])


@pytest.mark.parametrize(
    ("error_class", "expected_code"),
    [(OperationalError, 1), (UsageError, 2), (RejectedFile, 3)],
)
def test_error_classes_declare_their_exit_codes(error_class: type[Exception], expected_code: int) -> None:
    assert error_class.exit_code == expected_code


def test_error_classes_subclass_exception() -> None:
    assert issubclass(OperationalError, Exception)
    assert issubclass(UsageError, Exception)
    assert issubclass(RejectedFile, Exception)


def test_resolve_returns_the_run_function_of_the_named_command(monkeypatch: pytest.MonkeyPatch) -> None:
    def run(args: list[str]) -> int:
        return 0

    _register_command(monkeypatch, "probe", run)

    assert resolve("probe") is run


def test_resolve_rejects_a_name_that_is_not_a_command(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(UsageError):
        resolve("zzprobe-unknown-command")


@pytest.mark.parametrize("name", ["", "Probe", "../probe", "probe.sub", "9lives"])
def test_resolve_rejects_names_outside_the_command_grammar(name: str) -> None:
    with pytest.raises(UsageError):
        resolve(name)


def test_resolve_rejects_a_command_name_with_no_module() -> None:
    with pytest.raises(UsageError):
        resolve("zzprobe_absent")


def test_dispatch_with_no_arguments_returns_usage_exit_code() -> None:
    assert dispatch([]) == UsageError.exit_code


def test_dispatch_with_an_unknown_command_returns_usage_exit_code() -> None:
    assert dispatch(["zzprobe_absent"]) == UsageError.exit_code
