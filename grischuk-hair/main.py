import os
import asyncio
import threading
import uvicorn
from fastapi import FastAPI
from starlette.responses import PlainTextResponse

# ─── импорт твоего bot.py как модуля ───
import bot  # ← bot.py остаётся без изменений!

app = FastAPI()


@app.get("/health")
async def health() -> PlainTextResponse:
    return PlainTextResponse("OK")


def run_bot() -> None:
    """Запуск polling‑бота из bot.py в отдельном потоке."""
    bot.application.run_polling(drop_pending_updates=True)


@app.on_event("startup")
async def startup_event() -> None:
    # запускаем Telegram‑бота параллельно FastAPI
    threading.Thread(target=run_bot, daemon=True).start()


if __name__ == "__main__":
    # локальный запуск: uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
