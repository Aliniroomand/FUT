from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def auth_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔐 ورود", callback_data="auth:login")],
        [InlineKeyboardButton("🆕 ثبت‌نام", callback_data="auth:register")],
        [InlineKeyboardButton("⬅️ بازگشت به منو", callback_data="menu:back")],
    ])
