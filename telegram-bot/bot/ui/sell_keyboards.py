# bot/ui/sell_keyboards.py
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def get_amount_keyboard():
    keyboard = [
        [InlineKeyboardButton("❌ لغو پروسه فروش", callback_data="sell:cancel_process")],
        [InlineKeyboardButton("✅ تایید مقدار", callback_data="sell:confirm_amount")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirm_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔄 وارد کردن مقدار جدید", callback_data="sell:again_amount")],
        [InlineKeyboardButton("❌ لغو پروسه فروش", callback_data="sell:cancel_process")],
        [InlineKeyboardButton("✅ تایید مقدار", callback_data="sell:confirm_amount")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_after_cancel_keyboard():
    keyboard = [
        [InlineKeyboardButton("بازگشت به منو", callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)
