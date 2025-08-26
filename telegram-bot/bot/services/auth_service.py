# bot/services/auth_service.py

from bot.db import get_user_by_telegram_id

def is_user_logged_in(telegram_id: int) -> bool:
    """
    چک می‌کنه که آیا کاربر با توجه به telegram_id لاگین کرده یا نه
    """
    user = get_user_by_telegram_id(telegram_id)
    return user is not None and user.is_authenticated
