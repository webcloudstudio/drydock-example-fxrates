"""Argument validation for the fxrates command line.

`validate` runs before dispatch and rejects a malformed invocation with `UsageError`, so the caller
can exit 2 with empty stdout and one stderr line. It never opens a database or binds a socket.
"""

from __future__ import annotations

import re
from collections.abc import Collection

HELP_FLAG = "--help"
PORT_FLAG = "--port"
PORT_MIN = 1
PORT_MAX = 65535

# Exact positional argument counts for the commands whose stories are in the blueprint table.
_ARITY: dict[str, int] = {"init": 0, "load": 1, "fetch": 0}
_SERVE = "serve"


class UsageError(Exception):
    """A malformed invocation. The message is one line; its wording is not part of the contract."""


def validate(argv: list[str], registered: Collection[str] = ()) -> None:
    """Raise UsageError unless `argv` names a known command with well-formed arguments.

    `registered` holds the names of commands with a handler. A command outside the table above
    and outside `registered` is a usage error; a registered command outside the table is not
    arity-checked.
    """
    if not argv:
        raise UsageError("no command given; usage: fxrates <command> [arguments...]")
    command, rest = argv[0], list(argv[1:])
    if command == _SERVE:
        _validate_serve(rest)
    elif command in _ARITY:
        _validate_arity(command, rest)
    elif command not in registered:
        raise UsageError(f"unknown command: {command}")


def _validate_arity(command: str, rest: list[str]) -> None:
    if rest == [HELP_FLAG]:
        return
    expected = _ARITY[command]
    if len(rest) != expected:
        raise UsageError(f"{command} takes {expected} argument(s), got {len(rest)}")


def _validate_serve(rest: list[str]) -> None:
    if not rest or rest == [HELP_FLAG]:
        return
    if len(rest) != 2 or rest[0] != PORT_FLAG:
        raise UsageError(f"serve takes an optional {PORT_FLAG} <n>")
    _validate_port(rest[1])


def _validate_port(value: str) -> None:
    if not re.fullmatch(r"[0-9]+", value) or not PORT_MIN <= int(value) <= PORT_MAX:
        raise UsageError(f"{PORT_FLAG} must be an integer from {PORT_MIN} to {PORT_MAX}, got {value!r}")
