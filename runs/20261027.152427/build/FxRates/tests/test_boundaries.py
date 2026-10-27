"""Import boundary: the cli and app_server packages never import a database driver.

Only the generated `persistence` package reaches the store. This scans production source only.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

FORBIDDEN = {"sqlite3", "psycopg", "psycopg2", "sqlalchemy", "asyncpg"}
PACKAGES = ["cli", "app_server"]


def _imported_top_level_names(source: str) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module.split(".")[0])
    return names


@pytest.mark.parametrize("package", PACKAGES)
def test_package_imports_no_database_driver(project_root: Path, package: str) -> None:
    sources = sorted((project_root / package).rglob("*.py"))
    assert sources, f"{package} has no source files to check"

    offending = {
        path.relative_to(project_root).as_posix(): sorted(_imported_top_level_names(path.read_text(encoding="utf-8")) & FORBIDDEN)
        for path in sources
    }

    assert {path: names for path, names in offending.items() if names} == {}
