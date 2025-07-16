import os
import asyncio
from fastapi import FastAPI, Response
import uvicorn
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8000))

BOTT_URL = "https://forms.gle/Ut1eXu8P8fN1nbkv5"
BOT_URL = "https://forms.gle/1m7UdUy3u6rchxi4A"
WEBSITE_URL = "https://grischukhair.setmore.com/"

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Bot is running"}

@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return Response(status_code=200)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добрый день! Используйте команды из списка для работы со мной 😉\n"
        "/zapis – запись на услуги\n"
        "/vopros — вопрос мастеру\n"
        "/otzyv  — отзыв о работе мастера\n"
        "/adres  — адрес салона\n"
        "/uslugi — список и стоимость услуг\n"
        "/kontakty — контакты мастера\n"
        "/master — о мастере"
    )

async def zapis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Вы можете записаться на услуги по этой ссылке: {WEBSITE_URL}")

async def vopros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Задайте ваш вопрос здесь, и мастер свяжется с вами: {BOTT_URL}")

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
        "💇‍♀️ Екатерина Грищук — парикмахер‑универсал с обширным опытом работы!\n"
        "\nРаботает не по шаблону, а под ваш образ и стиль."
    )

application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("zapis", zapis))
application.add_handler(CommandHandler("vopros", vopros))
application.add_handler(CommandHandler("otzyv", otzyv))
application.add_handler(CommandHandler("uslugi", uslugi))
application.add_handler(CommandHandler("adres", adres))
application.add_handler(CommandHandler("kontakty", kontakty))
application.add_handler(CommandHandler("master", master))

async def run_bot():
    # Удаляем webhook (await!)
    await application.bot.delete_webhook(drop_pending_updates=True)
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

async def run_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=PORT, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(run_bot(), run_api())

if __name__ == "__main__":
    asyncio.run(main())
