#!/bin/sh
set -eu

MODEL_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin"
MODEL_SHA1="465707469ff3a37a2b9b8f89f2f99de7299dac"
PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON=${PYTHON:-"$PROJECT_ROOT/.venv/bin/python"}

if [ ! -x "$PYTHON" ]; then
  echo "Missing project environment. Run ./scripts/bootstrap.sh first." >&2
  exit 1
fi

MODEL_PATH=$(
  "$PYTHON" -c "from localweave.runtime import Settings; print(Settings.load().whisper_model_path)"
)
mkdir -p "$(dirname -- "$MODEL_PATH")"
curl -L --fail --output "$MODEL_PATH" "$MODEL_URL"
ACTUAL_SHA1=$(shasum "$MODEL_PATH" | awk '{print $1}')

if [ "$ACTUAL_SHA1" != "$MODEL_SHA1" ]; then
  echo "Model checksum verification failed." >&2
  exit 1
fi

chmod 600 "$MODEL_PATH"
echo "Installed verified multilingual base model at $MODEL_PATH"
