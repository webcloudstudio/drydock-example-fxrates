"""Foundation checks: interpreter, package import, manifest, and lockfile."""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

import fxrates_app


def _load_manifest(project_root: Path) -> dict:
    return tomllib.loads((project_root / "pyproject.toml").read_text(encoding="utf-8"))


def _dependency_names(specs: list[str]) -> set[str]:
    return {re.match(r"[A-Za-z0-9._-]+", spec).group(0).lower() for spec in specs}


def test_interpreter_is_python_311_or_newer() -> None:
    assert sys.version_info >= (3, 11)


def test_application_package_imports_by_name() -> None:
    assert fxrates_app.__name__ == "fxrates_app"


def test_manifest_requires_python_311_or_newer(project_root: Path) -> None:
    manifest = _load_manifest(project_root)

    assert manifest["project"]["requires-python"] == ">=3.11"


def test_manifest_declares_runtime_stack(project_root: Path) -> None:
    manifest = _load_manifest(project_root)

    names = _dependency_names(manifest["project"]["dependencies"])

    assert {"fastapi", "uvicorn", "httpx2"} <= names


def test_manifest_declares_pytest_as_dev_dependency(project_root: Path) -> None:
    manifest = _load_manifest(project_root)

    names = _dependency_names(manifest["dependency-groups"]["dev"])

    assert "pytest" in names


def test_lockfile_is_committed_at_project_root(project_root: Path) -> None:
    assert (project_root / "uv.lock").is_file()


def test_pytest_suite_is_configured_under_tests_directory(project_root: Path) -> None:
    manifest = _load_manifest(project_root)

    assert manifest["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests"]


def test_conftest_exists_in_tests_directory(project_root: Path) -> None:
    assert (project_root / "tests" / "conftest.py").is_file()
