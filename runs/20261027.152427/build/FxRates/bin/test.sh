#!/bin/sh
# CommandCenter Operation
# Name: Run Test Suite
# Type: batch

# --- Standard Preamble ---
set -eu
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$PROJECT_DIR/data/logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date '+%Y-%m-%d_%H%M%S')
SCRIPT_NAME=$(basename "$0" .sh)
LOG_FILE="$LOG_DIR/${SCRIPT_NAME}_${TIMESTAMP}.log"

echo "=== $SCRIPT_NAME started at $(date '+%Y-%m-%d %H:%M:%S') ===" | tee "$LOG_FILE"
echo "Arguments: $*" | tee -a "$LOG_FILE"
echo "Working dir: $PROJECT_DIR" | tee -a "$LOG_FILE"
echo "---" | tee -a "$LOG_FILE"

cd "$PROJECT_DIR"

if [ ! -f ".venv/bin/activate" ]; then
    echo "Environment missing: run 'uv sync' in $PROJECT_DIR first" | tee -a "$LOG_FILE" >&2
    exit 1
fi

# --- Run the declared test_command: pytest -q ---
# Calls the environment's pytest directly; sourcing activate trips `set -u`. Output is captured
# in full so the exit status of pytest is kept (a pipe would hide it).
set +e
"$PROJECT_DIR/.venv/bin/pytest" -q >"$LOG_FILE.pytest" 2>&1
STATUS=$?
set -e
cat "$LOG_FILE.pytest" | tee -a "$LOG_FILE"
rm -f "$LOG_FILE.pytest"

echo "=== $SCRIPT_NAME finished at $(date '+%Y-%m-%d %H:%M:%S') with status $STATUS ===" | tee -a "$LOG_FILE"
exit "$STATUS"
