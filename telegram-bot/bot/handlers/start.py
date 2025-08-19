from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.keyboards.main_menu import main_menu
from bot.keyboards.persistent import persistent_menu
from bot.storage import token_exists

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # support being called with either a Message update or CallbackQuery update
    query = update.callback_query if hasattr(update, 'callback_query') else None
    target = None
    if query and query.message:
        target = query.message
        await query.answer()
    elif update.message:
        target = update.message
    else:
        # nothing to reply to
        return

    user_id = update.effective_user.id if update.effective_user else None
    name = update.effective_user.first_name if update.effective_user else ""

    # show welcome only once per user session unless forced
    if context.user_data.get('seen_welcome'):
        # show main menu directly
        await target.reply_text(
            f"✅ خوش اومدی {name}!\n\nاز منوی زیر استفاده کن:",
            reply_markup=main_menu(user_id or 0)
        )
        return



    # persistent menu (near input) will be attached too
    persistent_kb = persistent_menu()

    await target.reply_text(
        f"✨ سلام {name}! خوبی؟ \n\n"
        "به اولین سامانه مدیریت سکه ( ادمین + هوش مصنوعی ) خوش اومدی💎\n\n"
    )

    # send persistent menu as a second message (it stays near input)
    await target.reply_text("از منوی زیر یکی رو انتخاب کن :", reply_markup=persistent_kb)

    context.user_data['seen_welcome'] = True

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "ℹ️ راهنما:\n\n"
        "🟢 /start - شروع و نمایش منو\n"
        "🟢 /help - نمایش همین راهنما\n"
        "🟢 /health - بررسی وضعیت ربات"
    )

async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ ربات فعال است و مشکلی ندارد.")
