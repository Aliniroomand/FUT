import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.config import settings
from bot.handlers.start import start_command, help_command, health_command
from bot.handlers.errors import error_handler

# text handlers
from bot.handlers.auth import register_start, register_name, login_start, login_process
from bot.handlers.main_menu import show_main_menu, view_transactions

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def post_init(application: Application) -> None:
    logging.info("Bot has started.")

async def post_stop(application: Application) -> None:
    logging.info("Bot has stopped.")

def main():
    application = Application.builder().token(settings.bot_token).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("health", health_command))

    # register message handlers for auth and main menu
    application.add_handler(MessageHandler(filters.Regex(r'^ثبت‌نام$'), register_start))
    application.add_handler(MessageHandler(filters.Regex(r'^ورود$'), login_start))

    # generic text handlers for multi-step flows (they check user_data['auth_flow'])
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, register_name))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, login_process))

    # main menu buttons
    application.add_handler(MessageHandler(filters.Regex(r'^مشاهده تراکنش‌ها$'), view_transactions))
    application.add_handler(MessageHandler(filters.Regex(r'^منو$|^منوی اصلی$'), show_main_menu))

    application.add_error_handler(error_handler)

    application.post_init = post_init
    application.post_stop = post_stop

    # Optional: HTTP_PROXY/HTTPS_PROXY can be set for Every Proxy usage
    application.run_polling(allowed_updates=None, close_loop=False)

if __name__ == "__main__":
    main()