# bot/ui/sell_purchase.py
# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def build_purchase_message(
    player_name: str,
    player_image_url: str | None,
    buy_price: int,
    transferable: int,
    multiplier: float,
    bn_min: int, bn_max: int,
    bid_min: int, bid_max: int,
    deadline_ts: float,
    tx_id: int | str,
) -> str:
    deadline = datetime.fromtimestamp(deadline_ts)
    lines = []
    lines.append("🟢 مرحله فروش: خرید و لیست‌کردن کارت در مارکت")
    lines.append("")
    if player_image_url:
        lines.append(f"🖼 عکس کارت: {player_image_url}")
    lines.append(f"👤 بازیکن: {player_name}")
    lines.append(f"💰 قیمت خرید تقریبی: {buy_price:,}")
    lines.append(f"📈 ضریب انتقال: {multiplier:g}x")
    lines.append(f"🎯 مقدار انتقال حدودی: {transferable:,}")
    lines.append("")
    lines.append("🛒 لطفاً کارت را با مشخصات زیر بخرید و لیست کنید:")
    lines.append(f"• Buy Now: بین {bn_min:,} تا {bn_max:,}")
    lines.append(f"• Bid: بین {bid_min:,} تا {bid_max:,}")
    lines.append("")
    lines.append(f"⏱ مهلت انجام: 1 دقیقه (تا {deadline.strftime('%H:%M:%S')})")
    lines.append("پس از خرید، روی «خریدم» بزنید. اگر نتوانستید بخرید، «لغوش کن نشد بخرم».")
    lines.append("")
    lines.append(f"🔖 شماره پیگیری موقت: {tx_id}")
    return "\n".join(lines)

def build_purchase_keyboard(tx_id: int | str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ خریدم", callback_data=f"sell:confirm:{tx_id}"),
            InlineKeyboardButton("❌ لغوش کن نشد بخرم", callback_data=f"sell:cancel_listing:{tx_id}"),
        ]
    ])

def build_purchase_expired() -> str:
    return "⛔️ زمان ۱ دقیقه‌ای به پایان رسید. لطفاً دوباره مقدار را وارد کنید یا به منو برگردید."
