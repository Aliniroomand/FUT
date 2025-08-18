# main.py
import logging
import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from bot.config import settings
from bot.handlers.start import start_command, help_command, health_command
from bot.handlers.errors import error_handler
from bot.proxy import get_requests_session, get_httpx_client

# text handlers
from bot.handlers.auth import register_start, register_name, login_start, login_process
from bot.handlers.main_menu import show_main_menu, view_transactions
from bot.handlers.start import phone_contact_handler, confirm_phone_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def post_init(application: Application) -> None:
    logging.info("Bot has started.")

async def post_stop(application: Application) -> None:
    logging.info("Bot has stopped.")

def main():
    # فقط یک Builder ساده بساز (بدون httpx_client)
    builder = Application.builder().token(settings.bot_token)
    application = builder.build()

    # هندلرهای اصلی
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("health", health_command))

    # هندلر تست پراکسی (از سشن‌های خودتون استفاده می‌کنه)
    async def proxy_test(update, context):
        # تست requests (sync)
        s = get_requests_session()
        try:
            r = s.get("https://api.telegram.org", timeout=10)
            text1 = f"requests status: {r.status_code}"
        except Exception as e:
            text1 = f"requests error: {e}"

        # تست httpx (async client از bot.proxy گرفته میشه)
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

    # هندلر دریافت شماره موبایل (contact)
    application.add_handler(MessageHandler(filters.CONTACT, phone_contact_handler))
    application.add_handler(
        MessageHandler(filters.Regex(r"^بله، شماره درست است$|^خیر، ارسال مجدد شماره$"), confirm_phone_handler)
    )

    # هندلرهای ثبت‌نام و ورود
    application.add_handler(MessageHandler(filters.Regex(r"^ثبت‌نام$"), register_start))
    application.add_handler(MessageHandler(filters.Regex(r"^ورود$"), login_start))
    # توجه: اگر هردو register_name و login_process هر دو با TEXT & ~COMMAND ثبت شده‌اند
    # ممکنه باهم تداخل کنند؛ اما من ساختار رو همانطور که ارسال کردی حفظ کردم.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, register_name))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, login_process))

    # هندلر منو و مشاهده تراکنش‌ها
    application.add_handler(MessageHandler(filters.Regex(r"^مشاهده تراکنش‌ها$"), view_transactions))
    application.add_handler(MessageHandler(filters.Regex(r"^منو$|^منوی اصلی$"), show_main_menu))

    # هندلر خطا
    application.add_error_handler(error_handler)

    # پست init و stop
    application.post_init = post_init
    application.post_stop = post_stop

    # اجرا
    application.run_polling()

if __name__ == "__main__":
    main()
