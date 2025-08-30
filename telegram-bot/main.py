# main.py (اصلاح‌شده) — ادغام ایمن BUY handlers و lifecycle
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
from bot.handlers.start import start_command, help_command, health_command, web_link_handler
from bot.handlers.errors import error_handler
from bot.proxy import get_requests_session, get_httpx_client
from bot.storage import token_exists
from bot.handlers.auth import register_start, text_handler, login_start, logout
from bot.handlers.main_menu import show_main_menu, view_transactions
from bot.keyboards.auth import auth_menu
from bot.keyboards.main_menu import main_menu

# تلاش برای وارد کردن buy handlers — اگر موجود نبود، placeholder می‌سازیم تا import error نداشته باشیم
try:
    from bot.handlers.buy import (
        start_buy,
        show_transfer_methods,
        buy_callback_router,
        buy_text_handler,
        buy_method_callback,
        buy_amount_handler,
        buy_confirm_callback,
        present_transfer_player,
        buy_list_callback,
        present_post_buy_options,
        buy_verify_callback,
        buy_mark_failed_callback,
        request_profile_confirmation,
        profile_input_handler,
        profile_confirm_callback,
        show_final_options,
        buy_new_transaction_callback,
    )
except Exception as e:
    logging.warning("Could not import buy handlers: %s. Using placeholders.", e)

    def _make_placeholder(name):
        async def _ph(update, context):
            # try to answer either callback_query or message
            try:
                if getattr(update, "callback_query", None):
                    await update.callback_query.answer()
                    await update.callback_query.edit_message_text("⚠️ قابلیت خرید هنوز آماده نیست. لطفاً بعداً تلاش کنید.")
                elif getattr(update, "message", None):
                    await update.message.reply_text("⚠️ قابلیت خرید هنوز آماده نیست. لطفاً بعداً تلاش کنید.")
            except Exception:
                # silent fallback
                logging.debug("placeholder %s could not send message", name)
        return _ph

    start_buy = _make_placeholder("start_buy")
    show_transfer_methods = _make_placeholder("show_transfer_methods")
    buy_method_callback = _make_placeholder("buy_method_callback")
    buy_amount_handler = _make_placeholder("buy_amount_handler")
    buy_confirm_callback = _make_placeholder("buy_confirm_callback")
    present_transfer_player = _make_placeholder("present_transfer_player")
    buy_list_callback = _make_placeholder("buy_list_callback")
    present_post_buy_options = _make_placeholder("present_post_buy_options")
    buy_verify_callback = _make_placeholder("buy_verify_callback")
    buy_mark_failed_callback = _make_placeholder("buy_mark_failed_callback")
    request_profile_confirmation = _make_placeholder("request_profile_confirmation")
    profile_input_handler = _make_placeholder("profile_input_handler")
    profile_confirm_callback = _make_placeholder("profile_confirm_callback")
    show_final_options = _make_placeholder("show_final_options")
    buy_new_transaction_callback = _make_placeholder("buy_new_transaction_callback")

# تلاش برای وارد کردن سرویس buy (برای lifecycle) — اگر نباشه، به‌صورت ایمن نادیده گرفته می‌شه
try:
    from bot.services import buy_service
except Exception:
    buy_service = None
    logging.info("buy_service not available; lifecycle hooks will skip buy_service init/shutdown")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def post_init(application: Application) -> None:
    logging.info("Bot has started.")
    # اگر buy_service دارای متد start است، آن را اجرا کن
    if buy_service is not None:
        start_fn = getattr(buy_service, "start", None)
        if callable(start_fn):
            try:
                await start_fn()
                logging.info("buy_service started successfully.")
            except Exception as e:
                logging.exception("BUY service startup error: %s", e)

async def post_stop(application: Application) -> None:
    logging.info("Bot has stopped.")
    if buy_service is not None:
        shutdown_fn = getattr(buy_service, "shutdown", None)
        if callable(shutdown_fn):
            try:
                await shutdown_fn()
                logging.info("buy_service shut down successfully.")
            except Exception as e:
                logging.exception("BUY service shutdown error: %s", e)

def main():
    builder = Application.builder().token(settings.bot_token)
    application = builder.build()

    # basic command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("health", health_command))

    # نمونه handler برای منوی شروع (callback from /start)
    async def menu_start_handler(update, context):
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id if query.from_user else 0
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

    # Register auth/menu handlers
    application.add_handler(CallbackQueryHandler(lambda u, c: u.callback_query.edit_message_text(
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=auth_menu()), pattern="^menu:auth$"))
    application.add_handler(CallbackQueryHandler(login_start, pattern="^auth:login$"))
    application.add_handler(CallbackQueryHandler(register_start, pattern="^auth:register$"))
    application.add_handler(CallbackQueryHandler(logout, pattern="^auth:logout$"))

    application.add_handler(CallbackQueryHandler(lambda u, c: u.callback_query.edit_message_text(
        "⬅️ بازگشت به منوی اصلی", reply_markup=main_menu(u.effective_user.id)), pattern="^menu:back$"))

    # persistent menu message handlers (placed before generic handlers)
    application.add_handler(MessageHandler(filters.Regex(r"^\s*شروع\s*$"), start_command))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:🏠\s*منو|منو اصلی|منو)$"), show_main_menu))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:🔑\s*ورود/ثبت‌نام|ورود/ثبت‌نام)$"), lambda u, c: u.message.reply_text('🔐 منوی احراز هویت:', reply_markup=auth_menu())))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:📊\s*نمایش تراکنش‌ها|نمایش تراکنش‌ها)$"), view_transactions))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:👤\s*پروفایل|پروفایل)$"), lambda u, c: u.message.reply_text('نمایش پروفایل در حال توسعه است.')))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:🌐\s*ورود به وبسایت|ورود به وبسایت)$"), web_link_handler))
    from bot.handlers.start import price_query_handler
    application.add_handler(MessageHandler(filters.Regex(r"^(?:💹\s*استعلام قیمت|استعلام قیمت)$"), price_query_handler))
    application.add_handler(MessageHandler(filters.Regex(r"^(?:❓\s*راهنما|راهنما)$"), help_command))

    # register the /buy entrypoints: callbacks from menu or text buttons
    application.add_handler(CallbackQueryHandler(start_buy, pattern="^menu:buy$"))
    # also register a text shortcut (e.g., "فروش سکه" or "💰 فروش سکه" depending on your labels)
    application.add_handler(MessageHandler(filters.Regex(r"^(?:🛒\s*💰 فروش سکه|💰 فروش سکه)$"), start_buy))

    # -------------------------
    # BUY HANDLERS (PRIORITY)
    # -------------------------
    # Make sure buy handlers are before generic text handlers so amount parsing works
    # Register specific buy-related callback handlers first so they are not caught by the generic router
    # handle transfer method selection (buy:method:<id>)
    application.add_handler(CallbackQueryHandler(buy_method_callback, pattern=r"^buy:method:"))
    # handle confirm amount (buy:confirm)
    application.add_handler(CallbackQueryHandler(buy_confirm_callback, pattern=r"^buy:confirm$"))
    # single router for other buy: callbacks (catch-all)
    application.add_handler(CallbackQueryHandler(buy_callback_router, pattern=r"^buy:"))
    # also accept buy_select and buy_cancel callback prefixes used by present_player flow
    # Accept only well-formed buy_select and buy_cancel callbacks: buy_select:<int>:(primary|fallback) or buy_cancel:<int>
    application.add_handler(CallbackQueryHandler(buy_callback_router, pattern=r'^(buy_select:\d+:(primary|fallback)|buy_cancel:\d+)$'))
    # text handler delegates amount parsing to buy_text_handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buy_text_handler), group=1)

    # Now the generic text handler (lower priority)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler), group=10)

    # error handler
    application.add_error_handler(error_handler)

    # attach lifecycle hooks for startup/shutdown
    application.post_init = post_init
    application.post_stop = post_stop

    return application

if __name__ == "__main__":
    app = main()
    print("BUY integration smoke-check: starting bot (Ctrl-C to stop).")
    app.run_polling()
