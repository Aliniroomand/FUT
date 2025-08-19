from telegram import ReplyKeyboardMarkup


def persistent_menu() -> ReplyKeyboardMarkup:
    # کیبورد ثابت نزدیکی input با ظاهری بهتر
    kb = [
        ["🏠 منو", "🔑 ورود/ثبت‌نام"],
        ["🛒 خرید سکه", "💰 فروش سکه"],
        ["📊 نمایش تراکنش‌ها", "👤 پروفایل"],
        ["🔁 شروع مجدد", "❓ راهنما"]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)
