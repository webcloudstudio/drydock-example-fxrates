"""Behavior tests for the project root: manifest, lock file and test launcher."""

import sys
import tomllib
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent


def _manifest() -> dict:
    return tomllib.loads((PROJECT_DIR / "pyproject.toml").read_text(encoding="utf-8"))


def test_manifest_declares_python_311_or_newer() -> None:
    assert _manifest()["project"]["requires-python"] == ">=3.11"
    assert sys.version_info >= (3, 11)


def test_manifest_declares_web_and_test_dependencies() -> None:
    dependencies = " ".join(_manifest()["project"]["dependencies"]).lower()

    for name in ("fastapi", "uvicorn", "pytest", "httpx2"):
        assert name in dependencies, name


def test_lock_file_is_committed_at_project_root() -> None:
    assert (PROJECT_DIR / "uv.lock").is_file()


def test_launcher_runs_pytest() -> None:
    script = (PROJECT_DIR / "bin" / "test.sh").read_text(encoding="utf-8")

    assert "pytest" in script
