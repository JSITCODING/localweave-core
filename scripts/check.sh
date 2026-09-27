#!/bin/sh
set -eu

PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON="$PROJECT_ROOT/.venv/bin/python"

if [ ! -x "$PYTHON" ]; then
  echo "Missing .venv. Run ./scripts/bootstrap.sh first." >&2
  exit 1
fi

"$PYTHON" -m pytest
"$PYTHON" -m ruff check "$PROJECT_ROOT/src" "$PROJECT_ROOT/tests"
"$PYTHON" -m mypy "$PROJECT_ROOT/src"
