from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("ورود / ثبت‌نام", callback_data="menu:auth")],
        [InlineKeyboardButton("خرید سکه", callback_data="menu:buy")],
        [InlineKeyboardButton("فروش سکه", callback_data="menu:sell")],
        [InlineKeyboardButton("نمایش تراکنش‌ها", callback_data="menu:tx")],
        [InlineKeyboardButton("پروفایل", callback_data="menu:profile")],
    ])