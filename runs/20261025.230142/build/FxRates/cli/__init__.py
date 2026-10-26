"""Callable command-line entry point for FxRates."""

from __future__ import annotations

import sys

from cli.commands import dispatch
from cli.parser import build_parser


def main(argv: list[str] | None = None) -> int:
    """Parse and dispatch arguments, returning the process status code."""
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code or 0)
    try:
        return dispatch(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
