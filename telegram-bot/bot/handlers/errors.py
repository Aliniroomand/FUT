import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Exception while handling an update:", exc_info=context.error)

    if update and hasattr(update, "effective_chat") and update.effective_chat:
        try:
            await update.effective_chat.send_message(
                "مشکلی پیش آمد. لطفاً دوباره تلاش کنید."
            )
        except Exception as e:
            logger.error("Failed to send error message: %s", e)