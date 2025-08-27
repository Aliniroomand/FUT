# # bot/handlers/sell.py
# # -*- coding: utf-8 -*-
# from __future__ import annotations
# import logging
# import time
# from typing import Optional

# from telegram import Update
# from telegram.ext import ContextTypes, ConversationHandler
# from telegram.constants import ParseMode

# from bot.storage import token_exists, user_tokens
# from bot.flows.sell_flows import SellFlow, SellState
# from bot.services import backend_client as backend
# from bot.services import trade_control
# from bot.services import futbin
# from bot.services import ws_client
# from bot.utils.parse import parse_amount_from_text
# from bot.ui import sell_messages as ui
# from bot.ui import sell_purchase as ui_purchase  
# from bot.config import settings

# SUPPORT_URL =" settings.SUPPORT_LINK"


# # ------------ helpers ------------
# def _flow(context: ContextTypes.DEFAULT_TYPE) -> SellFlow:
#     data = context.user_data.get("sell_flow")
#     if not isinstance(data, SellFlow):
#         data = SellFlow()
#         context.user_data["sell_flow"] = data
#     return data


# async def _ensure_logged_in(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
#     if not token_exists(update.effective_user.id):
#         await update.effective_message.reply_text("برای ادامه باید وارد حساب شوید /start")
#         return False
#     return True


# # --- bridge: call /start from a callback query safely ---
# class _UpdateFromCallback:
#     def __init__(self, update: Update, message):
#         self.update_id = getattr(update, "update_id", None)
#         self.effective_chat = update.effective_chat
#         self.effective_user = update.effective_user
#         self.effective_message = message
#         self.message = message


# async def _go_home_from_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str = "❌ پروسه فروش لغو شد ❌"):
#     query = update.callback_query
#     try:
#         await query.edit_message_text(text)
#     except Exception:
#         pass
#     from bot.handlers.start import start_command
#     fake_update = _UpdateFromCallback(update, query.message)
#     await start_command(fake_update, context)
#     return ConversationHandler.END


# # ------------ entry ------------
# async def handle_sell_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """نقطه شروع وقتی کاربر «فروش سکه» را می‌زند."""
#     if not await _ensure_logged_in(update, context):
#         return

#     flow = _flow(context)
#     flow.reset()
#     flow.state = SellState.CHECK_STATUS

#     status = await trade_control.get_status()
#     if status.get("selling_disabled"):
#         await update.effective_message.reply_text("⛔️ در حال حاضر فروش فعال نیست.")
#         flow.state = SellState.DONE
#         return

#     # روش انتقال را بپرس
#     flow.state = SellState.CHOOSE_METHOD
#     methods = await backend.list_transfer_methods()
#     text = ui.methods_prompt_text()
#     kb = ui.methods_keyboard(methods)
#     await update.effective_message.reply_text(text, reply_markup=kb)


# # ------------ callbacks ------------
# async def sell_callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if not await _ensure_logged_in(update, context):
#         return

#     query = update.callback_query
#     data = query.data or ""
#     await query.answer()
#     flow = _flow(context)

#     # انتخاب روش انتقال
#     if data.startswith("sell:method:"):
#         mid = int(data.split(":")[-1])
#         method = await backend.get_transfer_method(mid)
#         if not method or not method.get("is_active", True):
#             await query.edit_message_text("⛔️ این روش فعلاً غیرفعال است. یکی دیگر را انتخاب کنید.")
#             return
#         flow.method_id = mid
#         flow.method_name = method.get("name", "-")
#         flow.transfer_multiplier = float(method.get("transfer_multiplier", 1.0))
#         flow.state = SellState.ASK_AMOUNT
#         await query.edit_message_text(ui.build_amount_prompt(), reply_markup=ui.build_amount_keyboard())
#         return

#     # بازگشت/لغو عمومی
#     if data in ("sell:cancel", "sell:back_to_menu"):
#         flow.state = SellState.CANCELED
#         return await _go_home_from_callback(update, context, "❌ پروسه فروش لغو شد ❌")

#     # از نو وارد کردن مقدار
#     if data == "sell:again_amount":
#         logging.info("📌 دوباره مقدار انتخاب شد")
#         flow.amount = None
#         flow.state = SellState.ASK_AMOUNT
#         await query.edit_message_text(ui.build_amount_prompt(), reply_markup=ui.build_amount_keyboard())
#         return

#     # ✅ تأیید مقدار
#     if data == "sell:confirm_amount":
#         amount = flow.amount or 0
#         ranges = await backend.list_card_ranges()
#         selected = None
#         for r in ranges or []:
#             if int(r.get("min", 0)) <= amount <= int(r.get("max", 10**12)):
#                 selected = r
#                 break

#         if not selected:
#             await query.edit_message_text(
#                 "🔒 به دلیل تشخیص هوش مصنوعی برای رعایت امنیت اکانت شما، این مقدار بهتر است توسط ادمین انجام شود.",
#             await query.message.reply_text(ui.build_amount_prompt(), reply_markup=ui.build_amount_keyboard())
#             return

#         token = user_tokens.get(update.effective_user.id)
#         await backend.update_transaction(token, tx_id, {"status": "user_claimed_purchase"})
#         try:
#             await ws_client.emit("tx:claimed", {"tx_id": tx_id, "user_id": update.effective_user.id})
#         except Exception:
#             pass

#         flow.state = SellState.DONE
#         await query.edit_message_text("✅ دریافت شد. در حال بررسی خرید شما هستیم.")
#         await query.message.reply_text(ui.build_after_finish_text(), reply_markup=ui.build_after_finish_keyboard())
#         return

#     # کاربر لغو می‌کند (نشد بخرم)
#     if data.startswith("sell:cancel_listing:"):
#         tx_id = data.split(":")[-1]
#         token = user_tokens.get(update.effective_user.id)
#         await backend.update_transaction(token, tx_id, {"status": "user_canceled"})
#         try:
#             await ws_client.emit("tx:canceled", {"tx_id": tx_id, "user_id": update.effective_user.id})
#         except Exception:
#             pass
#         flow.state = SellState.CANCELED
#         await query.edit_message_text("لغو شد. می‌تونید دوباره تلاش کنید یا به منو برگردید.", reply_markup=ui.build_after_cancel_keyboard())
#         return

#     await query.answer("عملیات نامعتبر", show_alert=False)


# # ------------ text handler (amount) ------------
# async def sell_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     flow = _flow(context)
#     if flow.state != SellState.ASK_AMOUNT:
#         return

#     amount = parse_amount_from_text(update.effective_message.text)
#     if amount is None or amount <= 0:
#         await update.effective_message.reply_text("لطفاً مقدار را درست وارد کنید (مثلاً 150000).")
#         return

#     flow.amount = amount
#     flow.state = SellState.AWAIT_CONFIRM
#     text = f"💰 مقدار وارد شده: <b>{amount:,}</b>\n\nلطفاً انتخاب کنید:"
#     kb = ui.confirm_amount_keyboard()
#     await update.effective_message.reply_text(text, reply_markup=kb, parse_mode=ParseMode.HTML)
