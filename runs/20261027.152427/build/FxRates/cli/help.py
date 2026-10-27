"""Usage text for the fxrates commands: `<command> --help` prints it to standard output and exits 0.

Each command calls `print_help` before it opens the database or binds a socket. The text is two
lines: a usage line and a one-line summary.
"""

from __future__ import annotations

HELP: dict[str, tuple[str, str]] = {
    "init": (
        "usage: fxrates init",
        "summary: remove every stored rate and leave the schema in place.",
    ),
    "load": (
        "usage: fxrates load <file>",
        "summary: validate an ECB history CSV file and store its rates.",
    ),
    "fetch": (
        "usage: fxrates fetch",
        "summary: download the ECB history archive and store its rates.",
    ),
    "serve": (
        "usage: fxrates serve [--port <n>]",
        "summary: run the HTTP API in the foreground on 127.0.0.1 until SIGTERM.",
    ),
}


def print_help(command: str) -> int:
    """Print the usage line and summary for `command` to standard output and return 0."""
    usage_line, summary = HELP[command]
    print(usage_line)
    print(summary)
    return 0
