"""Command-line entry point for FxRates."""

from __future__ import annotations

import sys

from cli import commands
from cli.parser import build_parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)
    try:
        return commands.dispatch(args)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

