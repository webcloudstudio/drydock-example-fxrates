"""Command dispatch boundary; feature blocks provide command behavior."""

from __future__ import annotations

import argparse
import sys


def dispatch(args: argparse.Namespace) -> int:
    print(f"error: unknown command: {args.command}", file=sys.stderr)
    return 2
