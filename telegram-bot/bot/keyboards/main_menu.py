from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.storage import token_exists
from telegram import Update
from telegram.ext import ContextTypes


def main_menu(user_id: int) -> InlineKeyboardMarkup:
    
    
    
    """
    منوی اصلی هوشمند:
    اگر کاربر لاگین کرده باشه دکمه خروج، وگرنه ورود/ثبت‌نام
    """
    if token_exists(user_id):
        auth_button = InlineKeyboardButton("🚪  خروج از حساب", callback_data="auth:logout")
    else:
        auth_button = InlineKeyboardButton("🔑 ورود / ثبت‌نام", callback_data="menu:auth")

    return InlineKeyboardMarkup([
        [auth_button],
        [InlineKeyboardButton("🛒 خرید سکه", callback_data="menu:sell")],
        [InlineKeyboardButton("💰 فروش سکه", callback_data="menu:buy")],
        [InlineKeyboardButton("📊 نمایش تراکنش‌ها", callback_data="menu:tx")],
        [InlineKeyboardButton("👤 پروفایل", callback_data="menu:profile")],
        # [InlineKeyboardButton("🌐 ورود به وبسایت", url="#")],
    ])


