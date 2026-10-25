#!/bin/sh
# CommandCenter Operation
# Name: Run FxRates tests
# Type: batch

set -eu
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

if [ -x .venv/bin/pytest ]; then
    exec .venv/bin/pytest -q -c pyproject.toml
fi
exec python -m pytest -q -c pyproject.toml
