"""CLI entry point. Parsing and command behavior remain separate."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from .commands import dispatch
from .parser import build_parser


def main(argv: Sequence[str] | None = None) -> int:
    # Preserve the existing no-argument invocation contract for the project entry point.
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)
    return dispatch(args)
