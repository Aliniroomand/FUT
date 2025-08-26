# bot/handlers/sell.py
# -*- coding: utf-8 -*-
from __future__ import annotations
import asyncio
import time
from datetime import datetime, timedelta
from typing import Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode

from bot.storage import token_exists, user_tokens
from bot.flows.sell_flows import SellFlow, SellState
from bot.services import backend_client as backend
from bot.services import trade_control
from bot.services import futbin
from bot.services import ws_client
from bot.utils.parse import parse_amount_from_text
from bot.ui import sell_messages as ui
from bot.ui import sell_purchase as ui_purchase  
from bot.data.cards import get_player_card_meta, list_card_ranges
from bot.keyboards.sell_keyboards import sell_amount_keyboard
from bot.data.cards import get_player_card_meta as data_get_player_card_meta, list_card_ranges as data_list_card_ranges
from bot.config import settings

# --- ConversationHandler states ---
SELL_AMOUNT = range(1)


async def sell_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "SellYourFUT_Bot,\n\n"
        "🔢 لطفاً مقدار را به‌صورت عددی وارد کنید\n"
        "💡 مثلا به‌جای «۱۵۰۰ کا » فقط اینو بنویس: 1500 🔢"
    )
    return SELL_AMOUNT


async def sell_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("⚠️ لطفاً فقط عدد وارد کنید.")
        return SELL_AMOUNT

    amount = int(text)
    context.user_data["sell_amount"] = amount

    # نمایش کیبورد تایید / تغییر / لغو
    keyboard = sell_amount_keyboard(amount)
    await update.message.reply_text(
        f"💰 مقدار وارد شده: {amount}\n\n"
        "آیا تایید می‌کنید؟",
        reply_markup=keyboard,
    )
    return ConversationHandler.END


# 🛑 لغو پروسه فروش
async def cancel_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # پاک کردن دیتا کاربر
    context.user_data.clear()

    await query.edit_message_text("🛑 عملیات لغو شد.")
    # آوردن منوی اصلی (start)
    from bot.handlers.start import start_command
    await start_command(update, context)


# 🔄 وارد کردن مقدار جدید
async def again_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "SellYourFUT_Bot,\n\n"
        "🔢 لطفاً مقدار را به‌صورت عددی وارد کنید\n"
        "💡 مثلا به‌جای «۱۵۰۰ کا » فقط اینو بنویس: 1500 🔢"
    )
    return SELL_AMOUNT


# ✅ تایید مقدار
async def confirm_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    amount = context.user_data.get("sell_amount")
    if not amount:
        await query.edit_message_text("⚠️ خطا: مقداری یافت نشد. دوباره تلاش کنید.")
        return ConversationHandler.END

    # بررسی بازه مجاز
    min_amount, max_amount = 250, 5000
    if amount < min_amount or amount > max_amount:
        await query.edit_message_text(
            f"🚫 مقدار {amount} خارج از بازه مجاز ({min_amount}-{max_amount}) است.\n\n"
            f"🔒 به دلایل امنیتی، با پشتیبانی در ارتباط باشید:\n"
            f"{settings.SUPPORT_LINK}"
        )
        return ConversationHandler.END

    # اگر داخل بازه بود → گرفتن کارت‌ها
    cards = data_list_card_ranges()
    primary = data_get_player_card_meta(cards["primary"])
    secondary = data_get_player_card_meta(cards["secondary"])

    await query.edit_message_text(
        f"✅ مقدار تایید شد: {amount}\n\n"
        f"🎴 کارت اصلی: {primary}\n"
        f"🎴 کارت ثانویه: {secondary}"
    )
    return ConversationHandler.END
from bot.handlers.start import start_command


SUPPORT_URL = "https://t.me/your_support"  # TODO: از تنظیمات بردارید


# ------------ helpers ------------
def _flow(context: ContextTypes.DEFAULT_TYPE) -> SellFlow:
    data = context.user_data.get("sell_flow")
    if not isinstance(data, SellFlow):
        data = SellFlow()
        context.user_data["sell_flow"] = data
    return data


async def _ensure_logged_in(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not token_exists(update.effective_user.id):
        await update.effective_message.reply_text("برای ادامه باید وارد حساب شوید /start")
        return False
    return True


# ------------ entry ------------
async def handle_sell_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نقطه شروع وقتی کاربر «فروش سکه» را می‌زند."""
    if not await _ensure_logged_in(update, context):
        return

    flow = _flow(context)
    flow.reset()
    flow.state = SellState.CHECK_STATUS

    status = await trade_control.get_status()
    if status.get("selling_disabled"):
        await update.effective_message.reply_text("⛔️ در حال حاضر فروش فعال نیست.")
        flow.state = SellState.DONE
        return

    # روش انتقال را بپرس
    flow.state = SellState.CHOOSE_METHOD
    methods = await backend.list_transfer_methods()
    text = ui.methods_prompt_text()
    kb = ui.methods_keyboard(methods)
    await update.effective_message.reply_text(text, reply_markup=kb)


# ------------ callbacks ------------
async def sell_callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await _ensure_logged_in(update, context):
        return

    query = update.callback_query
    data = query.data or ""
    await query.answer()
    flow = _flow(context)

    # انتخاب روش انتقال
    if data.startswith("sell:method:"):
        mid = int(data.split(":")[-1])
        method = await backend.get_transfer_method(mid)
        if not method or not method.get("is_active", True):
            await query.edit_message_text("⛔️ این روش فعلاً غیرفعال است. یکی دیگر را انتخاب کنید.")
            return
        flow.method_id = mid
        flow.method_name = method.get("name", "-")
        flow.transfer_multiplier = float(method.get("transfer_multiplier", 1.0))
        flow.state = SellState.ASK_AMOUNT
        await query.edit_message_text(ui.build_amount_prompt(), reply_markup=ui.build_amount_keyboard())
        return

    # بازگشت/لغو عمومی
    if data in ("sell:cancel", "sell:back_to_menu"):
        flow.state = SellState.CANCELED
        await query.edit_message_text("لغو شد ✅")
        return

    # از نو وارد کردن مقدار
    if data == "sell:again_amount":
        flow.state = SellState.ASK_AMOUNT
        await query.edit_message_text(ui.build_amount_prompt(), reply_markup=ui.build_amount_keyboard())
        return

    # ✅ تأیید مقدار (اضافه‌شده از کد 1)
    if data == "sell:confirm_amount":
        amount = flow.amount or 0
        ranges = await backend.list_card_ranges()
        selected = None
        for r in ranges or []:
            if int(r.get("min", 0)) <= amount <= int(r.get("max", 10**12)):
                selected = r
                break

        if not selected:
            await query.edit_message_text(
                "🔒 به دلیل تشخیص هوش مصنوعی برای رعایت امنیت اکانت شما، این مقدار بهتر است توسط ادمین انجام شود.",
                reply_markup=ui.build_support_keyboard(SUPPORT_URL)
            )
            flow.state = SellState.DONE
            return

        # بازیکن‌ها رو ست کنیم
        p1 = selected.get("primary_player")
        p2 = selected.get("secondary_player")
        flow.primary_player = p1
        flow.secondary_player = p2

        flow.buy1 = futbin.get_player_price(p1["id"]) if p1 else None
        flow.buy2 = futbin.get_player_price(p2["id"]) if p2 else None
        flow.img1 = futbin.get_player_image_url(p1["id"]) if p1 else None
        flow.img2 = futbin.get_player_image_url(p2["id"]) if p2 else None

        multiplier = float(flow.transfer_multiplier or 1.0)
        flow.transferable1 = int((flow.buy1 or 0) * multiplier) if flow.buy1 else None
        flow.transferable2 = int((flow.buy2 or 0) * multiplier) if flow.buy2 else None

        flow.state = SellState.SHOW_OPTIONS
        text, kb = ui.build_options(
            amount=amount,
            p1=p1, p2=p2,
            buy1=flow.buy1, buy2=flow.buy2,
            img1=flow.img1, img2=flow.img2,
            multiplier=multiplier,
            t1=flow.transferable1, t2=flow.transferable2
        )
        await query.edit_message_text(text, reply_markup=kb, parse_mode=ParseMode.HTML)
        return

    # ❌ لغو پروسه فروش (همان کد 1)
    if data == "sell:cancel_process":
        flow.state = SellState.CANCELED
        await query.edit_message_text("پروسه فروش لغو شد ✅")
        return

    # 👇 بقیه منطق کد 2 بدون تغییر
    # کاربر نمی‌خواهد لیست کند
    if data == "sell:do_cancel":
        flow.state = SellState.CANCELED
        await query.edit_message_text(
            "باشه؛ اگر خواستید دوباره مقدار را وارد کنید یا به منو برگردید.",
            reply_markup=ui.after_decline_keyboard()
        )
        return

    # شروع مرحله لیست‌کردن
    if data == "sell:do_list":
        if not flow.primary_player and not flow.secondary_player:
            await query.edit_message_text("خطا: هنوز بازیکنی انتخاب نشده است.")
            return

        # ترجیح با primary است؛ اگر قیمت نداشت از secondary
        chosen = None
        buy_price = None
        if flow.buy1:
            chosen = flow.primary_player
            buy_price = flow.buy1
        elif flow.buy2:
            chosen = flow.secondary_player
            buy_price = flow.buy2
        else:
            await query.edit_message_text("⛔️ قیمت قابل اتکایی پیدا نشد. لطفاً مقدار دیگری امتحان کنید.")
            flow.state = SellState.ASK_AMOUNT
            await query.message.reply_text(ui.build_amount_prompt(flow.method_name), reply_markup=ui.build_amount_keyboard())
            return

        multiplier = float(flow.transfer_multiplier or 1.0)
        transferable = int(buy_price * multiplier)

        # محدوده‌های BN/Bid محافظه‌کارانه
        bn_min = max(150, int(transferable * 0.95))
        bn_max = max(bn_min, int(transferable * 1.05))
        bid_min = max(150, int(transferable * 0.80))
        bid_max = max(bid_min, int(transferable * 0.92))

        # ثبت تراکنش موقت
        token = user_tokens.get(update.effective_user.id)
        tx_payload = {
            "amount": int(flow.amount or 0),
            "method_id": flow.method_id,
            "player_id": chosen["id"],
            "player_name": chosen.get("name"),
            "estimated_buy_price": buy_price,
            "transfer_multiplier": multiplier,
            "bn_min": bn_min, "bn_max": bn_max,
            "bid_min": bid_min, "bid_max": bid_max,
            "status": "pending_user_purchase",
        }
        tx = await backend.create_transaction(token, tx_payload)
        tx_id = (tx or {}).get("id")
        flow.extra["tx_id"] = tx_id

        # گزارش لحظه‌ای به پنل ادمین
        try:
            await ws_client.emit("tx:new", {"tx_id": tx_id, "user_id": update.effective_user.id, "stage": "AWAIT_PURCHASE"})
        except Exception:
            pass

        # شمارش معکوس 1 دقیقه‌ای
        deadline = time.time() + 60
        flow.extra["deadline_ts"] = deadline
        flow.state = SellState.AWAIT_PURCHASE_CONFIRM

        text = ui_purchase.build_purchase_message(
            player_name=chosen.get("name", "-"),
            player_image_url=flow.img1 if chosen == flow.primary_player else flow.img2,
            buy_price=buy_price,
            transferable=transferable,
            multiplier=multiplier,
            bn_min=bn_min, bn_max=bn_max,
            bid_min=bid_min, bid_max=bid_max,
            deadline_ts=deadline,
            tx_id=tx_id or "-",
        )
        await query.edit_message_text(text, reply_markup=ui_purchase.build_purchase_keyboard(tx_id or "-"))
        return

    # کاربر تأیید می‌کند که خریده
    if data.startswith("sell:confirm:"):
        tx_id = data.split(":")[-1]
        deadline = float(flow.extra.get("deadline_ts", 0))
        if time.time() > deadline:
            flow.state = SellState.TIMEOUT
            await query.edit_message_text(ui_purchase.build_purchase_expired())
            # برگرداندن به وارد کردن مقدار
            flow.state = SellState.ASK_AMOUNT
            await query.message.reply_text(ui.build_amount_prompt(flow.method_name), reply_markup=ui.build_amount_keyboard())
            return

        # بروزرسانی تراکنش → در انتظار تأیید بک‌اند
        token = user_tokens.get(update.effective_user.id)
        await backend.update_transaction(token, tx_id, {"status": "user_claimed_purchase"})
        try:
            await ws_client.emit("tx:claimed", {"tx_id": tx_id, "user_id": update.effective_user.id})
        except Exception:
            pass

        flow.state = SellState.DONE
        await query.edit_message_text("✅ دریافت شد. در حال بررسی خرید شما هستیم. نتیجه در پروفایل/تراکنش‌ها ثبت می‌شود.")
        await query.message.reply_text(ui.build_after_finish_text(), reply_markup=ui.build_after_finish_keyboard())
        return

    # کاربر لغو می‌کند (نشد بخرم)
    if data.startswith("sell:cancel_listing:"):
        tx_id = data.split(":")[-1]
        token = user_tokens.get(update.effective_user.id)
        await backend.update_transaction(token, tx_id, {"status": "user_canceled"})
        try:
            await ws_client.emit("tx:canceled", {"tx_id": tx_id, "user_id": update.effective_user.id})
        except Exception:
            pass
        flow.state = SellState.CANCELED
        await query.edit_message_text("لغو شد. می‌تونید دوباره تلاش کنید یا به منو برگردید.", reply_markup=ui.build_after_cancel_keyboard())
        return

    # دستورات دیگر فروخته نشده
    await query.answer("عملیات نامعتبر", show_alert=False)


# ------------ text handler (amount) ------------
async def sell_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    flow = _flow(context)
    if flow.state != SellState.ASK_AMOUNT:
        return  # متن مربوط به این مرحله نیست

    amount = parse_amount_from_text(update.effective_message.text)
    if amount is None or amount <= 0:
        await update.effective_message.reply_text("لطفاً مقدار را درست وارد کنید (مثلاً 150000).")
        return

    flow.amount = amount

    # به‌جای رفتن مستقیم → اول مرحله تأیید مقدار
    flow.state = SellState.AWAIT_CONFIRM
    text = f"💰 مقدار وارد شده: <b>{amount:,}</b>\n\nلطفاً انتخاب کنید:"
    kb = ui.confirm_amount_keyboard()
    await update.effective_message.reply_text(text, reply_markup=kb, parse_mode=ParseMode.HTML)



async def sell_amount_options_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data.split(":")[1]

    # ذخیره مقدار وارد شده در دیتا
    amount = context.user_data.get("sell_amount")

    if choice == "cancel_process":
        # لغو عملیات → پیام + برگشت به منوی اصلی
        await query.edit_message_text("🛑 عملیات لغو شد.")
        return await start_command(update, context)

    elif choice == "again_amount":
        # دوباره وارد کردن مقدار
        await query.edit_message_text(
            "SellYourFUT_Bot,\n\n"
            "🔢 لطفاً مقدار را به‌صورت عددی وارد کنید\n"
            "💡 مثلا به‌جای «۱۵۰۰ کا » فقط اینو بنویس: 1500 🔢"
        )
        return  # ادامه فلو با MessageHandler انجام میشه

    elif choice == "confirm_amount":
        if not amount:
            return await query.edit_message_text("❗️ خطا: هیچ مقداری وارد نشده است.")

        # بازه‌ها رو چک می‌کنیم
        valid_ranges = list_card_ranges()
        if not any(r["min"] <= amount <= r["max"] for r in valid_ranges):
            support_url = "https://t.me/YourSupportLink"
            return await query.edit_message_text(
                f"🚨 مقدار وارد شده خارج از بازه‌های مجاز است.\n"
                f"برای بررسی بیشتر با پشتیبانی در ارتباط باشید:\n{support_url}"
            )

        # مقدار داخل بازه → نمایش اطلاعات کارت
        player_meta = get_player_card_meta(amount)
        text = (
            f"✅ مقدار {amount} تأیید شد.\n\n"
            f"👤 Primary Player: {player_meta['primary']}\n"
            f"👤 Secondary Player: {player_meta['secondary']}"
        )
        await query.edit_message_text(text)