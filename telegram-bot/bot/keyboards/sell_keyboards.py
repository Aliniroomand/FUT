from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def sell_amount_keyboard(amount=None):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ تایید مقدار", callback_data="sell:confirm_amount"),
            InlineKeyboardButton("🔄 وارد کردن دوباره", callback_data="sell:again_amount"),
        ],
        [
            InlineKeyboardButton("🛑 لغو", callback_data="sell:cancel_process")
        ]
    ])
    return InlineKeyboardMarkup(keyboard)
