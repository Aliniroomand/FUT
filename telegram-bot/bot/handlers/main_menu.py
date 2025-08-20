from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.main_menu import main_menu
from bot.keyboards.auth import auth_menu
from bot.storage import token_exists
from bot.keyboards.persistent import persistent_menu

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    هندلر برای متن '🏠 منو' یا هر فراخوانی مشابه
    """


async def view_transactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not token_exists(user_id):
        await update.message.reply_text("🔐 برای مشاهده تراکنش‌ها ابتدا وارد شوید.", reply_markup=auth_menu())
        return
    await update.message.reply_text("لیست تراکنش‌ها هنوز آماده نشده.")
