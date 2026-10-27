"""Packaging check: the `fxrates` launcher at the application root is executable and runs.

This is the one subprocess test in the suite; behavior is covered in-process in test_cli.py.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_launcher_is_executable_and_exits_with_usage_code(project_root: Path) -> None:
    launcher = project_root / "fxrates"

    assert launcher.is_file()
    assert os.access(launcher, os.X_OK)

    result = subprocess.run(
        [str(launcher)],
        cwd=project_root,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        timeout=60,
    )

    assert result.returncode == 2


def test_launcher_rejects_unknown_command_with_empty_stdout(project_root: Path) -> None:
    result = subprocess.run(
        [str(project_root / "fxrates"), "frobnicate"],
        cwd=project_root,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 2
    assert result.stdout == ""
