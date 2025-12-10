#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

VENV="${VENV:-$ROOT/.venv-build}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [ ! -d "$VENV" ]; then
  "$PYTHON_BIN" -m venv "$VENV"
fi

source "$VENV/bin/activate"
pip install --upgrade pip
pip install -r requirements-build.txt

pyinstaller --clean --noconfirm bcfeed.spec

APP_PATH="$ROOT/dist/bcfeed.app"
ZIP_PATH="$ROOT/dist/bcfeed-macos.zip"

if [ -d "$APP_PATH" ] && command -v ditto >/dev/null 2>&1; then
  ditto -c -k --keepParent "$APP_PATH" "$ZIP_PATH"
fi

echo "Built app bundle at $APP_PATH"
if [ -f "$ZIP_PATH" ]; then
  echo "Zipped app ready at $ZIP_PATH"
fi
