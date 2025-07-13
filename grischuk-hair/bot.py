import os
import asyncio
import uvicorn
from fastapi import FastAPI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Получаем токен из переменных окружения
TOKEN = os.environ.get('TOKEN')

app = FastAPI()
application = ApplicationBuilder().token(TOKEN).build()

BOTT_URL = "https://forms.gle/Ut1eXu8P8fN1nbkv5"
BOT_URL = "https://forms.gle/nm22TADvmSj9FmnL7"

# --- FastAPI endpoint для аптайма ---
@app.get("/health")
async def health_check():
    return {"status": "OK"}

# --- Telegram бота хендлеры ---
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
        "\n• Подравнивание волос — 40 р\n"
        "• Модельная стрижка — 50 р\n"
        "• Мужская стрижка — 35 р\n"
        "• Детская стрижка (до 12 лет) — 25 р\n"
        "• Окрашивание корней — 120 р\n"
        "• Окрашивание в 1 тон — 140 р\n"
        "• Окрашивание + стрижка — 160 р\n"
        "• Контуринг (коррекция AirTouch, тонировка включена) — 200–250 р\n"
        "• AirTouch / сложные техники (тонировка включена) — 320–380 р\n"
        "• Мелирование (тонировка включена) — 180–250 р\n"
        "\nТочная стоимость зависит от длины и густоты волос."
    )

async def adres(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📍 г. Минск, ул. Романовская Слобода, 9 (академия «Lilac», м. Фрунзенская)."
    )

async def kontakty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("☎️ Телефон / Telegram / Viber: +375 (29) 695‑72‑22")

async def master(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💇‍♀️ Екатерина Грищук — парикмахер‑универсал с обширным опытом работы! "
        "Работает не по шаблону, а под ваш образ и стиль."
    )

# Регистрируем хендлеры
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("vopros", vopros))
application.add_handler(CommandHandler("otzyv", otzyv))
application.add_handler(CommandHandler("uslugi", uslugi))
application.add_handler(CommandHandler("adres", adres))
application.add_handler(CommandHandler("kontakty", kontakty))
application.add_handler(CommandHandler("master", master))

async def run_bot():
    # Удаляем webhook, если используем polling
    await application.bot.delete_webhook(drop_pending_updates=True)
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

async def run_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(run_bot(), run_api())

if __name__ == "__main__":
    asyncio.run(main())
