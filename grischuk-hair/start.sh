#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# запускаем FastAPI‑сервер; PORT задаёт Render
exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"
