# bot/handlers/callbacks_sell.py
# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import time

from bot.flows.sell_flows import SellState
from bot.services import backend_client as backend, futbin, ws_client
from bot.storage import user_tokens
from bot.ui import sell_messages as ui, sell_purchase as ui_purchase

SUPPORT_URL = "https://t.me/your_support"  # TODO: از تنظیمات بخونید


def _flow(context: ContextTypes.DEFAULT_TYPE):
    return context.user_data.get("sell_flow")


async def handle_sell_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data or ""
    await query.answer()
    flow = _flow(context)

    # اینجا تمام if data == ... که توی sell.py داشتی میاد
    # دقیقا همون منطق — فقط از فایل جدا شده
    # مثلا:
    if data == "sell:again_amount":
        flow.state = SellState.ASK_AMOUNT
        await query.edit_message_text(ui.build_amount_prompt(), reply_markup=ui.build_amount_keyboard())
        return

    if data == "sell:cancel_process":
        flow.state = SellState.CANCELED
        await query.edit_message_text("پروسه فروش لغو شد ✅")
        return

    # و بقیه هم...
