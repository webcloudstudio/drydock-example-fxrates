"""ECB euro reference rate history: parse and validate the published CSV without writing anything."""

from ecb.history import Rate, parse_history

__all__ = ["Rate", "parse_history"]
