"""Behavior tests for bin/test.sh exit status, run against a scratch project."""

import shutil
import subprocess
from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def scratch_project(tmp_path: Path) -> Path:
    """Build a scratch project with the real launcher and the project venv."""
    (tmp_path / "bin").mkdir()
    shutil.copy(PROJECT_DIR / "bin" / "test.sh", tmp_path / "bin" / "test.sh")
    (tmp_path / ".venv").symlink_to(PROJECT_DIR / ".venv", target_is_directory=True)
    (tmp_path / "tests").mkdir()
    return tmp_path


def _run_launcher(project: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["sh", "bin/test.sh"],
        cwd=project,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )


def test_launcher_exits_zero_when_all_tests_pass(scratch_project: Path) -> None:
    (scratch_project / "tests" / "test_probe.py").write_text(
        "def test_passes() -> None:\n    assert 1 + 1 == 2\n", encoding="utf-8"
    )

    assert _run_launcher(scratch_project).returncode == 0


def test_launcher_exits_nonzero_when_a_test_fails(scratch_project: Path) -> None:
    (scratch_project / "tests" / "test_probe.py").write_text(
        "def test_fails() -> None:\n    assert False\n", encoding="utf-8"
    )

    assert _run_launcher(scratch_project).returncode != 0


def test_launcher_exits_nonzero_when_venv_is_missing(scratch_project: Path) -> None:
    (scratch_project / ".venv").unlink()

    assert _run_launcher(scratch_project).returncode != 0
