from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.main_menu import main_menu
from bot.storage import token_exists

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id if update.effective_user else None
    name = update.effective_user.first_name if update.effective_user else ""

    if user_id and token_exists(user_id):
        await update.message.reply_text(
            f"✅ خوش اومدی {name}!\n\n"
            "📌 شما قبلاً وارد شده‌اید.\n"
            "از منوی زیر استفاده کنید:",
            reply_markup=main_menu(user_id)
        )
    else:
        await update.message.reply_text(
            f"👋 سلام {name}!\n\n"
            "به اولین سامانه مدیریت سکه ادمین + هوش مصنوعی خوش اومدی💎\n\n"
            "برای شروع یکی از گزینه‌های زیر رو انتخاب کن:",
            reply_markup=main_menu(user_id or 0)
        )
        context.user_data['token_exists'] = False

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "ℹ️ راهنما:\n\n"
        "🟢 /start - شروع و نمایش منو\n"
        "🟢 /help - نمایش همین راهنما\n"
        "🟢 /health - بررسی وضعیت ربات"
    )

async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ ربات فعال است و مشکلی ندارد.")
