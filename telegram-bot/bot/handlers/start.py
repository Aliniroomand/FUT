from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.keyboards import main_menu
from bot.storage import is_logged_in

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id if update.effective_user else None

    if user_id is None or not is_logged_in(user_id):
        keyboard = ReplyKeyboardMarkup([["ورود", "ثبت‌نام"]], resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            "لطفاً ابتدا وارد شوید یا ثبت‌نام کنید.",
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            "به ربات خوش آمدید!",
            reply_markup=main_menu()
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "دستورات موجود:\n/start - شروع\n/help - راهنما\n/health - بررسی وضعیت ربات"
    )

async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Bot is alive")



