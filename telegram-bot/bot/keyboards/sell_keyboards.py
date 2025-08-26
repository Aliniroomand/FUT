from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def sell_amount_keyboard(amount=None):
    keyboard = [
        [
            InlineKeyboardButton("❌ لغو پروسه فروش", callback_data="sell:cancel_process"),
            InlineKeyboardButton("🔄 وارد کردن مقدار جدید", callback_data="sell:again_amount"),
        ],
        [
            InlineKeyboardButton("✅ تأیید مقدار", callback_data="sell:confirm_amount"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
