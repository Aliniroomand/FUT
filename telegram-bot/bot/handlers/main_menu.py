from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.main_menu import main_menu

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    هندلر برای متن '🏠 منو' یا هر فراخوانی مشابه
    """
    user_id = update.effective_user.id
    await update.message.reply_text("🏠 منوی اصلی:", reply_markup=main_menu(user_id))


async def view_transactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لیست تراکنش‌ها هنوز آماده نشده.")