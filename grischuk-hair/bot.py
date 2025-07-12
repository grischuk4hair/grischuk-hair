import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_URL = "https://forms.gle/TtgDh1pT58nDRX7K9"
BOTT_URL = "https://forms.gle/4bgKy3RbfHHoCe2j8"
ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# ─────────── handlers ───────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! Для работы с ботом используйте /vopros, /otzyv, /adres, /uslugi, /kontakty, /master."
    )


async def vopros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"❓ Задать вопрос мастеру можно тут: {BOT_URL}/index.html")


async def otzyv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"✍️ Оставить отзыв: {BOTT_URL}/feedback.html")


async def uslugi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"""✂️ Список и стоимость услуг:
        • Подравнивание волос- 40 р 
        • Модельная стрижка - 50 р
        • Мужская стрижка - 35 р
        • Детская стрижка (до 12 лет)- 25 р
        • Окрашивание корней - 120 р
        • Окрашивание в 1 тон- 140 р
        • Окрашивание + стрижка - 160 р
        • Контуринг(или коррекция AirTouch)(в стоимость входит тонировка) - 200-250 р
        • AirTouch/Сложные техники окрашивания(в стоимость входит тонировка) - 320-380р
        • Мелирование волос (в стоимость входит тонировка) - 180-250р 
         Точная стоимость определяется в зависимости от длины/густоты волос, выбора способа тонировки, наличия перерасхода красителя."""
    )


async def adres(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Адрес: г. Минск, ул. Романовская Слобода, 9. Академия «Lilac». Ⓜ️ Метро Фрунзенская.")


async def kontakty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"☎️ Телефон: +375 (29) 695-72-22.")


async def master(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💇‍♀️ Екатерина Грищук - парикмахер-универсал. За плечами - более 3-х лет опыта работы, сотни довольных клиентов и настоящее чувство стиля. Екатерина работает не по шаблону, а под вас - вашу энергию, образ жизни и настроение. В своей работе она сочетает мастерство, внимание к деталям и индивидуальный подход к каждому. Приходите за обновлением - будь то кардинальное преображение или лёгкое освежение образа.")


async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != ADMIN_CHAT_ID:
        await context.bot.send_message(
            chat_id=int(ADMIN_CHAT_ID),
            text=f"Вопрос от @{update.effective_user.username}: {update.message.text}",
        )
        await update.message.reply_text("Ваш вопрос отправлен!")


# ─────────── entry point ───────────
async def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("zapis", zapis))
    application.add_handler(CommandHandler("otzyv", otzyv))
    application.add_handler(CommandHandler("vopros", vopros))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))

    # Сбрасываем возможный webhook и чистим очередь апдейтов
    await application.bot.delete_webhook(drop_pending_updates=True)

    # Запускаем long‑polling (теперь конфликтов не будет)
    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
