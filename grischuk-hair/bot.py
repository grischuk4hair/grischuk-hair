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
    await update.message.reply_text(f"Задайте ваш вопрос здесь, и мастер свяжется с вами: {BOTT_URL}.")

async def otzyv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"✍️ Оставить отзыв можно на странице записи в разделе Отзывы: {WEBSITE_URL}")

async def uslugi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    links = {
        "Подравнивание волос": "https://grischukhair.setmore.com/services/8b5e91f2-442a-4fa9-ac0b-8a9c36455718",
        "Модельная стрижка": "https://grischukhair.setmore.com/services/e4284bc6-e71d-4471-b65b-64937a4f847b",
        "Мужская модельная стрижка": "https://grischukhair.setmore.com/services/f1d75d97-2426-4276-a2f4-0e2ed9303410",
        "Детская стрижка (до 12 лет)": "https://grischukhair.setmore.com/services/4678f44a-ad78-4043-8730-43f7163d370b",
        "Окрашивание корней полностью в один тон": "https://grischukhair.setmore.com/services/779eee3f-a487-45be-96cd-4b7d6c9f00d5",
        "Окрашивание волос полностью в один тон": "https://grischukhair.setmore.com/services/d1c9544b-64b2-43ea-9d28-bf7eb0269152",
        "Окрашивание волос один тон + стрижка (комплекс)": "https://grischukhair.setmore.com/services/1f2e831e-70e4-435f-a043-2afb4848d428",
        "Контуринг (коррекция AirTouch, тонировка включена)": "https://grischukhair.setmore.com/services/41c9ae3b-a8d1-4a7e-8ed2-a69c48b1a68c",
        "AirTouch / сложные техники (тонировка включена)": "https://grischukhair.setmore.com/services/2087ade8-b92f-43a0-beef-366715ef52ec",
        "Мелирование (тонировка включена)": "https://grischukhair.setmore.com/services/91d61b14-a4cf-4a78-bade-1b46305af860",
    }

    prices = {
        "Подравнивание волос": "40 р",
        "Модельная стрижка": "50 р",
        "Мужская модельная стрижка": "35 р",
        "Детская стрижка (до 12 лет)": "25 р",
        "Окрашивание корней полностью в один тон": "120 р",
        "Окрашивание волос полностью в один тон": "140 р",
        "Окрашивание волос один тон + стрижка (комплекс)": "160 р",
        "Контуринг (коррекция AirTouch, тонировка включена)": "200–250 р",
        "AirTouch / сложные техники (тонировка включена)": "320–380 р",
        "Мелирование (тонировка включена)": "180–250 р",
    }

    lines = ["✂️ <b>Список и стоимость услуг:</b>", ""]  # первая строка + пустая

    for name, url in links.items():
        price = prices.get(name, "")
        lines.append(f"• <a href=\"{url}\">{name}</a> — {price}")

    lines.append("") 
    lines.append("<i>Точная стоимость зависит от длины и густоты волос.</i>")

    text = "<br>".join(lines)
    await update.message.reply_text(text, parse_mode="HTML")

async def adres(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📍 г. Минск, ул. Романовская Слобода, 9 (академия «Lilac», м. Фрунзенская)."
    )

async def kontakty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("☎️ Телефон / Telegram / Viber: +375 (29) 695‑72‑22")

async def master(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Екатерина Грищук — парикмахер‑универсал с обширным опытом работы! За плечами мастера сотни довольных клиентов 💇‍♀️\n"
        "/Она обладает настоящим чувством стиля и работает не по шаблону, а под вас – вашу энергию, образ жизни и настроение!\n"
        "/В своей работе Екатерина сочетает мастерство, внимание к деталям и индивидуальный подход к каждому клиенту.\n"
        "/Приходите за обновлением: будь то кардинальное преображение или лёгкое освежение образа."
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
