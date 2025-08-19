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
    application.add_handler(CallbackQueryHandler(login_start, pattern="^auth:login$"))
    application.add_handler(CallbackQueryHandler(register_start, pattern="^auth:register$"))

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
