"""The `load` command: validate an ECB history file, store its rates, report the counts.

`parse_history` checks the whole file before the first write, so a rejected file exits 3 and stores
nothing. A file that cannot be opened or decoded exits 1 before any parsing or store access. Each rate is then written through the declared `rates.replace_rate` operation, which
replaces a rate already stored for the same date and currency, so loading a file twice leaves the
database unchanged.

The persistence library exposes no transaction operation, so each replace commits on its own. The
validation above is what keeps a rejected file from changing anything; a store failure part way
through a valid file is not rolled back.
"""

from __future__ import annotations

import sys

from cli.dispatcher import register_command
from cli.help import print_help
from fxrates_app.config import open_store
from fxrates_app.ecb import RejectedFile, parse_history

OPERATIONAL_FAILURE = 1
REJECTED = 3
HELP_FLAG = "--help"


def load(rest: list[str]) -> int:
    """Load the file named in `rest[0]` and return the exit code. The argument list is pre-validated."""
    if rest == [HELP_FLAG]:
        return print_help("load")
    try:
        with open(rest[0], encoding="utf-8", newline="") as handle:
            text = handle.read()
    except (OSError, UnicodeDecodeError) as error:
        print(f"error: cannot read {rest[0]}: {error}", file=sys.stderr)
        return OPERATIONAL_FAILURE
    try:
        rates = parse_history(text)
    except RejectedFile as error:
        print(f"error: {error}", file=sys.stderr)
        return REJECTED

    return store_and_report(rates)


def store_and_report(rates: list[tuple[str, str, str]]) -> int:
    """Store validated (date, currency, rate_text) rows and print the dates and rates counts.

    Shared by `load` and `fetch`, so both commands store and report the same way.
    """
    db = open_store()
    try:
        for date, currency, rate in rates:
            db.rates.replace_rate(date=date, currency=currency, rate=rate)
    finally:
        db.close()

    dates = {date for date, _, _ in rates}
    print("dates,rates")
    print(f"{len(dates)},{len(rates)}")
    return 0


register_command("load", load)
