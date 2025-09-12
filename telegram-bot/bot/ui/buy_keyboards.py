from typing import Dict, List  


def final_options_keyboard(user_id):
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    from bot.config import settings
    profile_url = getattr(settings, 'FRONTEND_PROFILE_URL', None)
    if profile_url:
        url = profile_url.format(user_id=user_id)
    else:
        url = getattr(settings, 'FRONTEND_URL', '') + '/profile'
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("انجام تراکنش جدید", callback_data="buy:new_transaction")],
        [InlineKeyboardButton("دیدن پروفایل کاربری", url=url)]
    ])
def profile_confirm_keyboard():
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("تأیید", callback_data="buy:confirm_profile")],
        [InlineKeyboardButton("لغو", callback_data="buy:cancel_profile")]
    ])
def verify_or_fail_keyboard(tx_id):
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅خریدم", callback_data=f"buy:verify:{tx_id}")],
        [InlineKeyboardButton("❌ لغوش کن نشد بخرم", callback_data=f"buy:mark_failed:{tx_id}")]
    ])
def list_or_decline_keyboard(player_id):
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ لیست کن", callback_data=f"buy:list:{player_id}")],
        [InlineKeyboardButton("❌ نه نمیخوام لیست نکن", callback_data="buy:decline_listing")]
    ])
def support_or_back_keyboard(chat_link):
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📞 گفتگو با پشتیبانی", url=chat_link)],
        [InlineKeyboardButton("↩️ بازگشت و تغییر مقدار", callback_data="buy:buy_method_callback")]
    ])
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict

def method_list_keyboard(methods: List[Dict]):
    buttons = []
    for m in methods:
        if m.get('is_active'):
            buttons.append([InlineKeyboardButton(f"✅{m['name']}✅", callback_data=f"buy:method:{m['id']}")])
        else:
            buttons.append([InlineKeyboardButton(f"🔒⛔️ {m['name']}⛔️🔒", callback_data=f"buy:method_disabled:{m['id']}")])
    return InlineKeyboardMarkup(buttons)

def confirm_amount_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("تایید", callback_data="buy:confirm")],
        [InlineKeyboardButton("انصراف", callback_data="buy:cancel")]
    ])


def choose_two_players_keyboard(has_second: bool = True):
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    buttons = [
        [InlineKeyboardButton(" 👤 بازیکن ۱" , callback_data="buy:choose:1")]
    ]
    if has_second:
        buttons.append([InlineKeyboardButton("👤 بازیکن ۲", callback_data="buy:choose:2")])
    buttons.append([InlineKeyboardButton("لغو ❌", callback_data="buy:cancel")])
    return InlineKeyboardMarkup(buttons)