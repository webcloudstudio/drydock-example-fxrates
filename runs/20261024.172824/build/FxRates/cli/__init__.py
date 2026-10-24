"""In-process command entry point."""

from __future__ import annotations

from cli.commands import dispatch
from cli.parser import build_parser


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and return the command exit status."""
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exc:
        # argparse owns usage text and status (normally 2), but the package entry point
        # remains callable in-process and returns that status to cli_runner.
        return int(exc.code or 0)
    return dispatch(args)
