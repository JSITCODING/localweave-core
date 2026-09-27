#!/bin/sh
set -eu

PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

if [ -z "${PYTHON_BIN:-}" ]; then
  for candidate in python3.13 python3.12 python3.11; do
    if command -v "$candidate" >/dev/null 2>&1; then
      PYTHON_BIN=$candidate
      break
    fi
  done
fi

PYTHON_BIN=${PYTHON_BIN:-python3}

if ! "$PYTHON_BIN" -c 'import sys; raise SystemExit(not ((3, 11) <= sys.version_info[:2] < (3, 14)))'; then
  echo "LocalWeave requires Python 3.11, 3.12, or 3.13." >&2
  echo "Set PYTHON_BIN to a supported interpreter and retry." >&2
  exit 1
fi

"$PYTHON_BIN" -m venv "$PROJECT_ROOT/.venv"
"$PROJECT_ROOT/.venv/bin/python" -m pip install --upgrade pip
"$PROJECT_ROOT/.venv/bin/python" -m pip install --editable "${PROJECT_ROOT}[dev]"

echo "LocalWeave development environment is ready with $PYTHON_BIN."
echo "Activate it with: source .venv/bin/activate"
