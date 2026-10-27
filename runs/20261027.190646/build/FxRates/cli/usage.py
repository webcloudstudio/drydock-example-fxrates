"""Argument validation for the fxrates command line, run before any command handler.

parse() returns the command name and the arguments its run() receives as parsed values. Every
violation raises UsageError, which the dispatcher maps to exit status 2 with nothing on stdout.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence

from cli.errors import UsageError

DEFAULT_PORT = 8000
_INTEGER = re.compile(r"-?[0-9]+")

Rule = Callable[[str, list[str]], list[str | int]]


def parse(argv: Sequence[str]) -> tuple[str, list[str | int]]:
    """Validate argv and return (command name, parsed arguments); raise UsageError on a violation."""
    if not argv:
        raise UsageError("no command given")
    name, rest = argv[0], list(argv[1:])
    rule = _RULES.get(name)
    if rule is None:
        # A name outside the declared table is valid only when a command module provides it.
        # Imported here because cli.dispatch imports this module.
        from cli.dispatch import resolve

        resolve(name)
        return name, rest
    return name, rule(name, rest)


def _no_arguments(name: str, rest: list[str]) -> list[str | int]:
    if rest:
        raise UsageError(f"{name} takes no arguments")
    return []


def _load(name: str, rest: list[str]) -> list[str | int]:
    if any(arg.startswith("-") for arg in rest):
        raise UsageError(f"{name} has an unknown option")
    if len(rest) != 1:
        raise UsageError(f"{name} takes exactly one path")
    return [rest[0]]


def _serve(name: str, rest: list[str]) -> list[str | int]:
    if not rest:
        return [DEFAULT_PORT]
    if len(rest) != 2 or rest[0] != "--port":
        raise UsageError(f"{name} accepts only --port <n>")
    if not _INTEGER.fullmatch(rest[1]):
        raise UsageError(f"--port value {rest[1]!r} is not an integer")
    return [int(rest[1])]


_RULES: dict[str, Rule] = {
    "init": _no_arguments,
    "fetch": _no_arguments,
    "load": _load,
    "serve": _serve,
}
