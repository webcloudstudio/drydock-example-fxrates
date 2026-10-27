"""Command registry and dispatch.

Command stories register a handler under a command name at import time. `main` hands the
remaining arguments to the handler and returns the handler's exit code.
"""

from __future__ import annotations

import sys
from collections.abc import Callable

from cli import usage

USAGE_ERROR = 2

_handlers: dict[str, Callable[[list[str]], int]] = {}


def register_command(name: str, handler: Callable[[list[str]], int]) -> None:
    """Map a command name to its handler; registering a name again replaces the handler."""
    _handlers[name] = handler


def main(argv: list[str] | None = None) -> int:
    """Validate `argv`, dispatch `argv[0]` to its registered handler, and return the exit code."""
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        usage.validate(args, _handlers)
    except usage.UsageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return USAGE_ERROR
    handler = _handlers.get(args[0])
    if handler is None:
        print(f"error: command not available in this build: {args[0]}", file=sys.stderr)
        return USAGE_ERROR
    return handler(args[1:])
