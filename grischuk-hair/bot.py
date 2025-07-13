import os
import asyncio
from fastapi import FastAPI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import threading

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

BOTT_URL = "https://forms.gle/WNs4Fk5wabFmTuhm8"
BOT_URL = "https://forms.gle/RcHQFGpzmVvQfYsUA"

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "OK"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте!\n"
        "/vopros — вопрос\n"
        "/otzyv  — отзыв\n"
        "/adres  — адрес\n"
        "/uslugi — услуги\n"
        "/kontakty — контакты\n"
        "/master — о мастере"
    )


async def vopros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Напишите ваш вопрос здесь: {BOTT_URL}")


async def otzyv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"✍️ Оставить отзыв: {BOT_URL}")


async def uslugi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✂️ Список и стоимость услуг:\n"
        "• Подравнивание волос — 40 р\n"
        "• Модельная стрижка — 50 р\n"
        "• Мужская стрижка — 35 р\n"
        "• Детская стрижка (до 12 лет) — 25 р\n"
        "• Окрашивание корней — 120 р\n"
        "• Окрашивание в 1 тон — 140 р\n"
        "• Окрашивание + стрижка — 160 р\n"
        "• Контуринг (коррекция AirTouch, тонировка включена) — 200–250 р\n"
        "• AirTouch / сложные техники (тонировка включена) — 320–380 р\n"
        "• Мелирование (тонировка включена) — 180–250 р\n"
        "\nТочная стоимость зависит от длины и густоты волос."
    )


async def adres(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📍 г. Минск, ул. Романовская Слобода, 9 (академия «Lilac», м. Фрунзенская)."
    )


async def kontakty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("☎️ Телефон / Telegram / Viber: +375 (29) 695‑72‑22")


async def master(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💇‍♀️ Екатерина Грищук — парикмахер‑универсал с обширным опытом работы! "
        "Работает не по шаблону, а под ваш образ и стиль."
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("vopros", vopros))
    application.add_handler(CommandHandler("otzyv", otzyv))
    application.add_handler(CommandHandler("uslugi", uslugi))
    application.add_handler(CommandHandler("adres", adres))
    application.add_handler(CommandHandler("kontakty", kontakty))
    application.add_handler(CommandHandler("master", master))

   def run_bot():
    application.run_polling()

# ────── точка входа для uvicorn и polling ──────
if __name__ == "__main__":
    # Запускаем polling в отдельном потоке, чтобы не блокировать FastAPI
    threading.Thread(target=run_bot, daemon=True).start()

    # Запускаем FastAPI сервер
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
