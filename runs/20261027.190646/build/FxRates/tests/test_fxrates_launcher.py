"""Packaging tests for the fxrates executable at the application root."""

import os
import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LAUNCHER = PROJECT_DIR / "fxrates"


def test_launcher_is_executable_and_starts_with_an_interpreter_line() -> None:
    assert LAUNCHER.is_file()
    assert os.access(LAUNCHER, os.X_OK)
    assert LAUNCHER.read_text(encoding="utf-8").startswith("#!")


def test_launcher_exits_with_the_usage_code_for_an_unknown_command() -> None:
    # The one subprocess test for packaging: the launcher runs the real entry point.
    completed = subprocess.run(
        [str(LAUNCHER), "zzprobe-unknown-command"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )

    assert completed.returncode == 2
    assert completed.stdout == ""
