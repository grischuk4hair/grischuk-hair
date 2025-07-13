#!/usr/bin/env bash
set -e  # если какая-то команда падает — останавливаем скрипт

# Переходим в папку, где лежит сам start.sh
cd "$(dirname "$0")"

# Создаём/активируем виртуальное окружение (если нужно)
python3 -m venv .venv
source .venv/bin/activate

# Ставим зависимости
pip install -r requirements.txt

# Перед запуском бота окончательно снимаем возможный webhook и чистим очередь
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/deleteWebhook" \
     -d "drop_pending_updates=true" >/dev/null

# Запускаем FastAPI + polling (bot.py запускает uvicorn)
exec uvicorn bot:app --host 0.0.0.0 --port ${PORT:-8000}
