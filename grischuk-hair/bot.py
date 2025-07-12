import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_URL = "https://example.onrender.com/web"
ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Используйте /zapis, /otzyv или /vopros.")

async def zapis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Записаться можно тут: {BOT_URL}/index.html")

async def otzyv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Оставить отзыв: {BOT_URL}/feedback.html")

async def vopros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напишите ваш вопрос:")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != ADMIN_CHAT_ID:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Вопрос от @{update.effective_user.username}:
{update.message.text}")
        await update.message.reply_text("Ваш вопрос отправлен!")

app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("zapis", zapis))
app.add_handler(CommandHandler("otzyv", otzyv))
app.add_handler(CommandHandler("vopros", vopros))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))
app.run_polling()
