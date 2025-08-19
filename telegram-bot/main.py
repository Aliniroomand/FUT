# main.py
import logging
import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from bot.config import settings
from bot.handlers.start import start_command, help_command, health_command
from bot.handlers.errors import error_handler
from bot.proxy import get_requests_session, get_httpx_client
from telegram.ext import ChatMemberHandler, filters
from bot.storage import token_exists

# auth handlers
from bot.handlers.auth import register_start, text_handler, login_start, logout
from bot.handlers.main_menu import show_main_menu, view_transactions
from bot.keyboards.auth import auth_menu
from bot.keyboards.main_menu import main_menu

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def post_init(application: Application) -> None:
    logging.info("Bot has started.")

async def post_stop(application: Application) -> None:
    logging.info("Bot has stopped.")

def main():
    builder = Application.builder().token(settings.bot_token)
    application = builder.build()

    # دستورات اصلی
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("health", health_command))

    # هندلر تست پراکسی
    async def proxy_test(update, context):
        s = get_requests_session()
        try:
            r = s.get("https://api.telegram.org", timeout=10)
            text1 = f"requests status: {r.status_code}"
        except Exception as e:
            text1 = f"requests error: {e}"

        try:
            client = await get_httpx_client()
            try:
                r = await client.get("https://api.telegram.org", timeout=10)
                text2 = f"httpx status: {r.status_code}"
            except Exception as e:
                text2 = f"httpx error: {e}"
        except Exception as e:
            text2 = f"httpx error: {e}"

        await update.message.reply_text(text1 + "\n" + text2)

    application.add_handler(CommandHandler("proxytest", proxy_test))

    # Handle the welcome "شروع" button from /start with real logic
    async def menu_start_handler(update, context):
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id if query.from_user else 0
        # if logged in, show main menu; otherwise show auth menu
        if token_exists(user_id):
            await query.edit_message_text(
                "خوش آمدید! منوی اصلی:",
                reply_markup=main_menu(user_id)
            )
        else:
            await query.edit_message_text(
                "برای ادامه لطفاً وارد شوید یا ثبت‌نام کنید:",
                reply_markup=auth_menu()
            )

    application.add_handler(CallbackQueryHandler(menu_start_handler, pattern="^menu:start$"))

    # Reply keyboard 'شروع' button handler (user can press it instead of typing /start)
    application.add_handler(MessageHandler(filters.Regex(r"^شروع$"), start_command))

    # ==========================
    # CallbackQuery handlers
    # ==========================

    # منوی اصلی -> auth
    application.add_handler(
        CallbackQueryHandler(
            lambda u, c: u.callback_query.edit_message_text(
                "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
                reply_markup=auth_menu()
            ),
            pattern="^menu:auth$"
        )
    )

    # ورود و ثبت‌نام
    async def auth_router(update, context):
        query = update.callback_query
        await query.answer()
        data = query.data or ""
        # route to appropriate auth handler
        if data == 'auth:login':
            await login_start(update, context)
            return
        if data == 'auth:register':
            await register_start(update, context)
            return
        # fallback: edit message to auth menu
        await query.edit_message_text("لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=auth_menu())

    application.add_handler(CallbackQueryHandler(auth_router, pattern="^auth:.*$"))

    # لاگ‌اوت
    application.add_handler(CallbackQueryHandler(logout, pattern="^auth:logout$"))

    # بازگشت به منوی اصلی
    application.add_handler(
        CallbackQueryHandler(
            lambda u, c: u.callback_query.edit_message_text(
                "⬅️ بازگشت به منوی اصلی",
                reply_markup=main_menu(u.effective_user.id)
            ),
            pattern="^menu:back$"
        )
    )

    # هندلرهای متنی مربوط به auth
    application.add_handler(MessageHandler(filters.Regex(r"^ثبت‌نام$"), register_start))
    application.add_handler(MessageHandler(filters.Regex(r"^ورود$"), login_start))

    # -- persistent menu helper handlers (moved before the generic text handler)
    async def open_auth_menu(update, context):
        await update.message.reply_text('🔐 منوی احراز هویت:', reply_markup=auth_menu())

    async def buy_placeholder(update, context):
        user_id = update.effective_user.id
        if not token_exists(user_id):
            await update.message.reply_text('🔐 برای استفاده از خرید ابتدا وارد شوید.', reply_markup=auth_menu())
            return
        await update.message.reply_text('صفحه خرید در حال توسعه است.')

    async def sell_placeholder(update, context):
        user_id = update.effective_user.id
        if not token_exists(user_id):
            await update.message.reply_text('🔐 برای استفاده از فروش ابتدا وارد شوید.', reply_markup=auth_menu())
            return
        await update.message.reply_text('صفحه فروش در حال توسعه است.')

    async def profile_placeholder(update, context):
        user_id = update.effective_user.id
        if not token_exists(user_id):
            await update.message.reply_text('🔐 برای مشاهده پروفایل ابتدا وارد شوید.', reply_markup=auth_menu())
            return
        await update.message.reply_text('نمایش پروفایل در حال توسعه است.')

    async def restart_bot(update, context):
        # Only clear non-essential session flags, keep login/profile/jwt_token
        keys_to_keep = {'jwt_token', 'user_profile', 'access_token', 'refresh_token', 'is_logged_in', 'phone_number', 'email'}
        keys_to_remove = [k for k in context.user_data.keys() if k not in keys_to_keep]
        for k in keys_to_remove:
            context.user_data.pop(k, None)
        await update.message.reply_text('ربات ریست شد. ♻️')

    # Register persistent menu buttons BEFORE the generic text handler
    application.add_handler(MessageHandler(filters.Regex(r"^\s*شروع\s*$"), start_command))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:🏠\s*منو|منو اصلی|منو)$"), show_main_menu))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:🔑\s*ورود/ثبت‌نام|ورود/ثبت‌نام)$"), open_auth_menu))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:🛒\s*خرید سکه|خرید سکه)$"), buy_placeholder))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:💰\s*فروش سکه|فروش سکه)$"), sell_placeholder))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:📊\s*نمایش تراکنش‌ها|نمایش تراکنش‌ها)$"), view_transactions))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:👤\s*پروفایل|پروفایل)$"), profile_placeholder))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:🔁\s*شروع مجدد|شروع مجدد)$"), restart_bot))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:❓\s*راهنما|راهنما)$"), help_command))

    # هندلر پیام‌های متنی در جریان auth
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    # منو و تراکنش‌ها
    application.add_handler(MessageHandler(filters.Regex(r"^مشاهده تراکنش‌ها$"), view_transactions))
    application.add_handler(MessageHandler(filters.Regex(r"^منو$|^منوی اصلی$"), show_main_menu))

    # هندلر خطا
    application.add_error_handler(error_handler)

    # post init / stop
    application.post_init = post_init
    application.post_stop = post_stop

    # اجرای ربات
    application.run_polling()

if __name__ == "__main__":
    main()
