"""Command line entry point. Feature command implementations are added later."""

from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command line application."""
    del argv
    raise NotImplementedError("CLI commands are introduced by later build blocks")
