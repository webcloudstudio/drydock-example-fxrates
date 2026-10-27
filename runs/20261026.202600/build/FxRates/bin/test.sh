#!/bin/sh
# CommandCenter Operation
# Name: Run project tests
# Type: batch
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
mkdir -p data/logs
STAMP=$(date '+%Y-%m-%d_%H%M%S')
LOG="data/logs/test_${STAMP}.log"
TMP=${TMPDIR:-/tmp}/fxrates-test-$$
trap 'rm -f "$TMP"' EXIT HUP INT TERM
{
    printf 'timestamp=%s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')"
    printf 'arguments=%s\n' "$*"
    printf 'working_directory=%s\n' "$ROOT"
} | tee "$LOG"
if .venv/bin/python -m pytest -q "$@" >"$TMP" 2>&1; then
    cat "$TMP" | tee -a "$LOG"
    printf 'completed=%s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" | tee -a "$LOG"
    exit 0
else
    STATUS=$?
    cat "$TMP" | tee -a "$LOG"
    printf 'completed=%s status=%s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$STATUS" | tee -a "$LOG"
    exit "$STATUS"
fi
