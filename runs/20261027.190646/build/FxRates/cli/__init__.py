"""Command-line entry point. main() returns the exit code; only the launcher exits the process."""

from __future__ import annotations

import sys

from cli.dispatch import dispatch


def main(argv: list[str] | None = None) -> int:
    """Dispatch argv (default: the process arguments without the program name) and return the exit code."""
    if argv is None:
        argv = sys.argv[1:]
    return dispatch(argv)
