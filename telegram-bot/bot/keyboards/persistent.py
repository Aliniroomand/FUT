from telegram import ReplyKeyboardMarkup


def persistent_menu() -> ReplyKeyboardMarkup:
    kb = [
        ["🏠 منو", "🔑 ورود/ثبت‌نام"],
        ["🛒 خرید سکه", "💰 فروش سکه"],
        ["📊 نمایش تراکنش‌ها", "👤 پروفایل"],
        ["🌐 ورود به وبسایت", "💹 استعلام قیمت"]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)
