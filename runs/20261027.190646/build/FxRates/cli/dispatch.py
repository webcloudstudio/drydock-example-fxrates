"""Command resolution and the mapping from raised errors to exit codes."""

from __future__ import annotations

import importlib
import re
import sys
from collections.abc import Callable, Sequence

from cli.errors import OperationalError, RejectedFile, UsageError
from cli.usage import parse

COMMAND_PACKAGE = "cli.commands"
_COMMAND_NAME = re.compile(r"[a-z][a-z0-9_]*")
_MAPPED_ERRORS = (OperationalError, UsageError, RejectedFile)

Handler = Callable[[list[str]], int]


def execute(handler: Handler, args: Sequence[str]) -> int:
    """Call handler(args) and return its result; map a raised expected error to its exit code.

    The error's message goes to stderr as one line. Nothing is written to stdout on failure.
    """
    try:
        return handler(list(args))
    except _MAPPED_ERRORS as exc:
        message = " ".join(str(exc).split())
        print(f"error: {message}", file=sys.stderr)
        return exc.exit_code


def resolve(name: str) -> Handler:
    """Return the run() of the cli.commands module named by the first argument."""
    if not _COMMAND_NAME.fullmatch(name):
        raise UsageError(f"unknown command {name!r}")
    module_name = f"{COMMAND_PACKAGE}.{name}"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        # Only a missing command module is a usage error; a broken import inside one propagates.
        if exc.name == module_name:
            raise UsageError(f"unknown command {name!r}") from None
        raise
    return module.run


def dispatch(argv: Sequence[str]) -> int:
    """Validate argv, route it to its command module and return the exit code."""

    def route(args: list[str]) -> int:
        name, command_args = parse(args)
        return resolve(name)(command_args)

    return execute(route, argv)
