"""Callable CLI runner that captures streams without spawning a process."""

from __future__ import annotations

import contextlib
import io

from cli import main


def cli_runner(*args: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(args))
    return code, out.getvalue(), err.getvalue()
