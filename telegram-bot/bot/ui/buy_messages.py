PROFILE_PROMPT_MSG = "لطفاً نام کامل و اطلاعات حساب بانکی خود را وارد کنید."
PROFILE_WARNING_MSG = "⚠️ دقت کنید: هرگونه اشتباه در مشخصات بانکی ممکن است منجر به واریز به حساب اشتباه شود و مسئولیت بر عهده شماست."
PROFILE_CONFIRM_MSG = "آیا اطلاعات زیر را تأیید می‌کنید؟"
PROFILE_SUCCESS_MSG = "✅ اطلاعات پروفایل و تراکنش با موفقیت ثبت شد."
BUY_DISABLED_MSG = "⛔️ در حال حاضر سیستم خرید فعال نیست."
BUY_CHOOSE_METHOD_MSG = "لطفاً روش انتقال را انتخاب کنید:"
BUY_METHODS_INFO_MSG = "⚠️❓ کدام روش انتقال را می‌خواهید استفاده کنید؟\n\n متدهای فعال بر اساس تشخیص امنیتی 🤖هوش مصنوعی +👤ادمین انتخاب شده‌اند. ⚠️ "
BUY_METHODS_ERROR_MSG = "⛔️ خطا در دریافت متدهای انتقال. لطفاً بعداً تلاش کنید."
BUY_METHOD_DISABLED_MSG = "⛔️ هوش مصنوعی این روش را به دلیل امنیتی مسدود کرده ،متد هایی که فعال و کم ریسک تر هستند را انتخاب کنید  ... ⛔️"

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Tuple

def out_of_range_text(admin_username: str) -> Tuple[str, InlineKeyboardMarkup]:
    text = ("⚠️ به دلیل تشخیص هوش مصنوعی و برای حفظ امنیت اکانت شما، "
            "انتقال این مقدار بهتر است توسط ادمین انجام شود.⚠️")
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 چت با پشتیبانی", url=f"https://t.me/{admin_username}")],
        [InlineKeyboardButton("بازگشت به منوی اصلی", callback_data="sell:back_to_menu")]
        ])
    return text, kb


def build_card_info_text(selected_range: dict, primary_card: dict, fallback_card: dict, transfer_multiplier: float, amount: float) -> str:
    
    """سازندهٔ متن نمایش کارت در فلوی خرید.
    پارامترها:
      - selected_range: دیکشنری بازه انتخاب‌شده
      - primary_card: دادهٔ بازیکن اصلی (مطالعه‌شده از backend)
      - fallback_card: کارت پشتیبان (در صورت وجود)
      - transfer_multiplier: ضریب انتقال (برای محاسبه مقدار انتقال تقریبی)
      - amount: مقدار ورودی کاربر
    تابع سعی می‌کند اولین مقدار قیمت از فیلدهای متداول را بخواند:
      estimated_value, futbin_price, buy_now, buyNow, LCPrice
    و درصورت نبودن مقدار، متن مناسبی نمایش می‌دهد.
    """
    # Helper to normalize price keys
    def _get_price_from_card(card):
        if not card or not isinstance(card, dict):
            return None
        for key in ("estimated_value", "futbin_price", "buy_now", "buyNow", "LCPrice", "price"):
            v = card.get(key)
            if v is None:
                continue
            try:
                return int(v)
            except Exception:
                try:
                    s = str(v).replace(",", "").strip()
                    if s.isdigit():
                        return int(s)
                except Exception:
                    continue
        return None

    player = primary_card.get("player") if isinstance(primary_card, dict) else {}
    name = player.get("name") or primary_card.get("name") or "نامشخص"
    rating = player.get("rating") or primary_card.get("rating") or "—"
    buy_now = _get_price_from_card(primary_card)
    fallback_buy_now = _get_price_from_card(fallback_card)

    lines = []
    lines.append(f"🔹 پیشنهاد انتقال برای: {name} — رتبه: {rating}")
    if buy_now is not None:
        approx_transfer = int(buy_now * (transfer_multiplier or 1))
        lines.append(f"💰 قیمت تقریبی (Buy Now): {buy_now:,}")
        lines.append(f"📦 مقدار انتقال تقریبی (با ضریب {transfer_multiplier}): {approx_transfer:,}")
    elif fallback_buy_now is not None:
        lines.append(f"💰 قیمت تقریبی (از کارت پشتیبان): {fallback_buy_now:,}")
    else:
        lines.append("⚠️ قیمت تقریبی در دسترس نیست — ممکن است Futbin پاسخگو نباشد.")

    # Add some metadata if present
    if primary_card.get("contract"):
        lines.append(f"📄 قرارداد: {primary_card.get('contract')}")
    if primary_card.get("owners") is not None:
        lines.append(f"👥 مالکین: {primary_card.get('owners')}")
    if primary_card.get("games") is not None:
        lines.append(f"🎮 بازی‌ها: {primary_card.get('games')}")
    if selected_range:
        lines.append(f"🔎 بازه انتخاب‌شده: {selected_range.get('name') or selected_range.get('id', 'نامشخص')}")

    # elapsed time formatting if provided
    elapsed = primary_card.get("fetched_at_elapsed") or primary_card.get("elapsed") or primary_card.get("age")
    if elapsed:
        lines.append(f"⏱ زمان از لحظه دریافت: {elapsed}")

    # final instruction
    lines.append("\nشما 60 ثانیه وقت دارید تا کارت را 'لیست کن' یا 'نه، نمی‌خوام'.")
    return "\n".join(lines)
