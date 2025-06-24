import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from data import TIME_MEANINGS

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cat, callback_data=f"cat|{cat}")] for cat in TIME_MEANINGS]
    await update.message.reply_text("Выбери категорию времени:", reply_markup=InlineKeyboardMarkup(keyboard))

async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, category = query.data.split("|")

    buttons = [
        [InlineKeyboardButton(time_str, callback_data=f"time|{category}|{time_str}")]
        for time_str in TIME_MEANINGS[category]
    ]

    await query.message.edit_text(
        text=f"Выбери время из категории: {category}",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def time_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, category, time_str = query.data.split("|")

    meaning = TIME_MEANINGS[category][time_str]
    await query.message.edit_text(
        text=f"🕒 {time_str}\n\n📖 {meaning}"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(category_handler, pattern="^cat\|"))
    app.add_handler(CallbackQueryHandler(time_handler, pattern="^time\|"))
    print("Бот запущен...")
    app.run_polling()
