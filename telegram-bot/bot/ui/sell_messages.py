# bot/ui/sell_messages.py
"""
UI texts for selling flow (Farsi)
"""

def get_sell_entry_text():
    return (
        "SellYourFUT_Bot,\n\n"
        "🔢 لطفاً مقدار را به‌صورت عددی وارد کنید\n"
        "💡 مثلا به‌جای «۱۵۰۰ کا » فقط اینو بنویس: 1500 🔢"
    )

def get_invalid_amount_text():
    return "⚠️ لطفاً فقط عدد وارد کنید."

def get_amount_confirm_text(amount):
    return f"💰 مقدار وارد شده: {amount}\n\nآیا تایید می‌کنید؟"

def get_amount_out_of_range_text(amount, min_amount, max_amount, support_link):
    return (
        f"🚫 مقدار {amount} خارج از بازه مجاز ({min_amount}-{max_amount}) است.\n\n"
        f"🔒 به دلایل امنیتی، با پشتیبانی در ارتباط باشید:\n{support_link}"
    )

def get_card_info_text(amount, player_meta):
    return (
        f"✅ مقدار تایید شد: {amount}\n\n"
        f"🎴 کارت اصلی: {player_meta['primary']}\n"
        f"🎴 کارت ثانویه: {player_meta['secondary']}"
    )

def get_cancelled_text():
    return "🛑 عملیات لغو شد."
# bot/ui/sell_messages.py
from typing import List, Tuple, Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes

def transaction_closed_text(kind: str) -> str:
    # kind: "buying" or "selling"
    if kind == "selling":
        return ("⛔️ در حال حاضر سیستم فروش سکه فعال نیست.\n"
                "برای اطلاع از زمان فعال‌سازی دوباره با پشتیبانی در تماس باشید.")
    return ("⛔️ در حال حاضر سیستم خرید سکه فعال نیست.\n"
            "برای اطلاع از زمان فعال‌سازی دوباره با پشتیبانی در تماس باشید.")

def methods_prompt_text() -> str:
    return (
        "❓ کدام روش انتقال را می‌خواهید استفاده کنید؟\n\n"
        "🔹 متدهای غیرفعال نمایش داده می‌شوند اما انتخاب‌شدنی نیستند.\n\n"
        "🤖 متدهای فعال بر اساس <b>تشخیص امنیتی هوش مصنوعی</b> و <b>ادمین</b> انتخاب شده‌اند."
    )

def methods_keyboard(methods: List[dict]) -> InlineKeyboardMarkup:
    buttons: List[List[InlineKeyboardButton]] = []
    for m in methods:
        name = m.get("name", "نامشخص")
        mid = m.get("id")
        active = m.get("is_active", False)
        label = f"{name} {'✅ فعال' if active else '❌ غیرفعال'}"
        if active and mid is not None:
            buttons.append([
                InlineKeyboardButton(label, callback_data=f"sell:method:{str(mid)}")
            ])
        else:
            buttons.append([
                InlineKeyboardButton(label, callback_data="sell:method:disabled")
            ])
    buttons.append([InlineKeyboardButton("لغو", callback_data="sell:cancel")])
    return InlineKeyboardMarkup(buttons)


def build_amount_prompt() -> str:
    return "🔢 لطفاً مقدار را به‌صورت عددی وارد کنید\n \n  💡 مثلا به‌جای «۱۵۰۰ کا » فقط اینو بنویس: 1500 🔢"

def build_amount_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("بازگشت", callback_data="sell:back_to_menu")],
        [InlineKeyboardButton("لغو", callback_data="sell:cancel")]
    ])

# تایید مقدار بعد از وارد کردن
def confirm_amount_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("✅ تأیید مقدار", callback_data="sell:confirm_amount"),
        ],
        [
            InlineKeyboardButton("🔄 وارد کردن مقدار جدید", callback_data="sell:enter_new_amount"),
        ],
        [
            InlineKeyboardButton("❌ لغو پروسه فروش", callback_data="sell:cancel_process"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def out_of_range_text(admin_username: str) -> Tuple[str, InlineKeyboardMarkup]:
    text = ("به دلیل تشخیص هوش مصنوعی و برای حفظ امنیت اکانت شما، "
            "انتقال این مقدار بهتر است توسط ادمین انجام شود.")
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 چت با پشتیبانی", url=f"https://t.me/{admin_username}")],
        [InlineKeyboardButton("بازگشت به منوی اصلی", callback_data="sell:back_to_menu")]
    ])
    return text, kb

def player_option_text(player_name: str, buy_price: Optional[int], transferable: Optional[float]) -> str:
    return (
        f"بازیکن: {player_name or 'نامشخص'}\n"
        f"قیمت پیشنهادی (Futbin): {buy_price if buy_price is not None else 'نامشخص'}\n"
        f"میزان قابل انتقال تقریبی: {int(transferable) if transferable is not None else 'نامشخص'}\n\n"
        "⚠️ تا ۱ دقیقه فرصت دارید یک گزینه را انتخاب کنید:⚠️"
    )

def list_or_cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ لیست کن", callback_data="sell:do_list")],
        [InlineKeyboardButton("❌ لیست نکن", callback_data="sell:do_cancel")],
    ])

def after_decline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("بازگشت به منوی اصلی", callback_data="sell:back_to_menu")],
        [InlineKeyboardButton("وارد کردن مقدار جدید", callback_data="sell:again_amount")],
    ])


def build_options(
    amount: int,
    p1: Optional[dict], p2: Optional[dict],
    buy1: Optional[int], buy2: Optional[int],
    img1: Optional[str], img2: Optional[str],
    multiplier: float,
    t1: Optional[int], t2: Optional[int],
):
    """ساخت پیام و کیبورد انتخاب بازیکن بعد از وارد کردن مقدار."""
    parts = [f"💰 مقدار وارد شده: {amount}"]

    buttons = []

    if p1:
        txt1 = player_option_text(p1.get("name"), buy1, t1)
        if img1:
            txt1 += f"\n🖼 <a href='{img1}'>مشاهده تصویر</a>"
        parts.append(txt1)
        buttons.append([InlineKeyboardButton(f"انتخاب {p1.get('name', '-')}", callback_data="sell:do_list")])

    if p2:
        txt2 = player_option_text(p2.get("name"), buy2, t2)
        if img2:
            txt2 += f"\n🖼 <a href='{img2}'>مشاهده تصویر</a>"
        parts.append(txt2)
        buttons.append([InlineKeyboardButton(f"انتخاب {p2.get('name', '-')}", callback_data="sell:do_list")])

    # دکمه‌های عمومی
    buttons.append([InlineKeyboardButton("❌ لغو", callback_data="sell:do_cancel")])
    buttons.append([InlineKeyboardButton("↩️ وارد کردن مقدار جدید", callback_data="sell:again_amount")])

    text = "\n\n".join(parts)
    return text, InlineKeyboardMarkup(buttons)

# 
def build_amount_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ تأیید مقدار", callback_data="sell:confirm_amount")],
        [InlineKeyboardButton("🔄 وارد کردن مقدار جدید", callback_data="sell:again_amount")],
        [InlineKeyboardButton("❌ لغو پروسه فروش", callback_data="sell:cancel_flow")]
    ])




# شبیه دیتابیس موقت کارت‌ها
CARDS = {
    "primary": {"number": "6037-69**-****-1234", "name": "کارت اصلی"},
    "fallback": {"number": "5892-10**-****-5678", "name": "کارت پشتیبان"},
}

async def ask_for_card(update: Update, context: ContextTypes.DEFAULT_TYPE, amount: str):
    """نمایش کارت‌ها بعد از وارد کردن مبلغ"""
    keyboard = []

    # کارت اصلی همیشه وجود دارد
    primary_card = CARDS.get("primary")
    keyboard.append([
        InlineKeyboardButton(
            f"{primary_card['name']} | {primary_card['number']}",
            callback_data=f"choose_card:primary:{amount}"
        )
    ])

    # اگر کارت پشتیبان تعریف شده بود، اضافه می‌کنیم
    fallback_card = CARDS.get("fallback")
    if fallback_card:
        keyboard.append([
            InlineKeyboardButton(
                f"{fallback_card['name']} | {fallback_card['number']}",
                callback_data=f"choose_card:fallback:{amount}"
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "💳 لطفا کارت مورد نظر برای انتقال را انتخاب کنید:",
        reply_markup=reply_markup
    )