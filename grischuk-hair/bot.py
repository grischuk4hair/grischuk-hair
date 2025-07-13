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

# ────── конфигурация ────────────────────────────────────────────────────────
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("TELEGRAM_ADMIN_CHAT_ID", "0"))
BOT_URL = "https://forms.gle/RcHQFGpzmVvQfYsUA"

# ────── handlers ────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! Используйте команды:\n"
        "/vopros  — задать вопрос\n"
        "/otzyv   — оставить отзыв\n"
        "/adres   — наш адрес\n"
        "/uslugi  — услуги и цены\n"
        "/kontakty — контакты\n"
        "/master  — о мастере"
    )


async def vopros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напишите ваш вопрос:")


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
    await update.message.reply_text("☎️ +375 (29) 695‑72‑22")


async def master(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💇‍♀️ Екатерина Грищук — парикмахер‑универсал с 3+ годами опыта. "
        "Работает не по шаблону, а под ваш образ и стиль."
    )


async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_CHAT_ID:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"Вопрос от @{update.effective_user.username}: {update.message.text}",
        )
        await update.message.reply_text("Ваш вопрос отправлен!")


# ────── точка входа ─────────────────────────────────────────────────────────
async def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("vopros", vopros))
    application.add_handler(CommandHandler("otzyv", otzyv))
    application.add_handler(CommandHandler("uslugi", uslugi))
    application.add_handler(CommandHandler("adres", adres))
    application.add_handler(CommandHandler("kontakty", kontakty))
    application.add_handler(CommandHandler("master", master))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message)
    )

    # удаляем возможный webhook и чистим очередь, чтобы не было Conflict
    await application.bot.delete_webhook(drop_pending_updates=True)

    # запускаем long‑polling
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
