from functools import wraps
from bot.storage import is_logged_in
from telegram import Update
from telegram.ext import ContextTypes


def login_required(handler):
    @wraps(handler)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        user_id = user.id if user else None
        if not user_id or not is_logged_in(user_id):
            if update.message:
                await update.message.reply_text("❌ لطفاً ابتدا وارد شوید یا ثبت‌نام کنید.")
            elif update.effective_chat:
                await update.effective_chat.send_message("❌ لطفاً ابتدا وارد شوید یا ثبت‌نام کنید.")
            return
        return await handler(update, context, *args, **kwargs)
    return wrapper
