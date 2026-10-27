#!/bin/sh
# CommandCenter Operation
# Name: Run Test Suite
# Type: batch

# Runs the project test suite (pytest -q) from the application root in the
# project .venv. The exit status is pytest's: nonzero when any test fails.
# No "set -u": the venv activate script reads unset variables such as OSTYPE.
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

if [ ! -f .venv/bin/activate ]; then
    echo "test.sh: .venv not found; create it with 'uv sync'" >&2
    exit 1
fi

. .venv/bin/activate
exec pytest -q
