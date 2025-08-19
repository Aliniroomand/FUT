from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.main_menu import main_menu
from bot.keyboards.auth import auth_menu
from bot.storage import token_exists

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    هندلر برای متن '🏠 منو' یا هر فراخوانی مشابه
    """
    user_id = update.effective_user.id
    if not token_exists(user_id):
        await update.message.reply_text("🔐 برای دسترسی به منو ابتدا باید وارد شوید.", reply_markup=auth_menu())
        return
    await update.message.reply_text("🏠 منوی اصلی:", reply_markup=main_menu(user_id))


async def view_transactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not token_exists(user_id):
        await update.message.reply_text("🔐 برای مشاهده تراکنش‌ها ابتدا وارد شوید.", reply_markup=auth_menu())
        return
    await update.message.reply_text("لیست تراکنش‌ها هنوز آماده نشده.")