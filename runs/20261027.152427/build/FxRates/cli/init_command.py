"""The `init` command: empty the rates store, print nothing, exit 0.

The schema is provisioned by the DATABASE step, so init never runs DDL or opens a driver. It
removes every stored rate through the declared `rates.delete_from_date` operation, passing a date
earlier than any publication, and leaves the table in place with no rows.
"""

from __future__ import annotations

from cli.dispatcher import register_command
from cli.help import print_help
from fxrates_app.config import open_store

EARLIEST_DATE = "0000-01-01"
HELP_FLAG = "--help"


def init(rest: list[str]) -> int:
    """Remove every stored rate and return 0. The argument list is validated before dispatch."""
    if rest == [HELP_FLAG]:
        return print_help("init")
    db = open_store()
    try:
        db.rates.delete_from_date(from_date=EARLIEST_DATE)
    finally:
        db.close()
    return 0


register_command("init", init)
