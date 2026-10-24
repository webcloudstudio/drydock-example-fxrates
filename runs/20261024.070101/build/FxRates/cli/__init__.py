"""Command-line entry point for FxRates.

Command behavior belongs in this package and delegates application work to
shared services; it does not access the database directly.
"""

from __future__ import annotations


def main(argv: list[str] | None = None) -> int:
    """Callable CLI entry point; command dispatch is added with CLI behavior."""
    del argv
    return 2
