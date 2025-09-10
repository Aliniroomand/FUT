async def buy_text_handler(update, context):
    # Handle plain text inputs for BUY flow (amount entry)
    flow = context.user_data.get('buy_flow')
    if not flow:
        return
    if flow.state == BuyState.ASK_AMOUNT:
        return await buy_amount_handler(update, context)
    # Ignore other text when not in buy amount state


async def buy_callback_router(update, context):
    query = update.callback_query
    if not query:
        return
    data = query.data or ""
    # try to clear callback spinner
    try:
        await query.answer()
    except Exception:
        pass

    flow = context.user_data.get('buy_flow')

    # Return to amount entry
    if data == "buy:buy_method_callback":
        logging.info("buy_callback_router: received buy:buy_method_callback for user %s", getattr(update.effective_user, 'id', None))
        # ensure we have a flow; if not, create a minimal ASK_AMOUNT flow
        if not flow:
            flow = BuyFlow(state=BuyState.ASK_AMOUNT)
            context.user_data['buy_flow'] = flow
            # convert None values to empty string
            flow_dict = {k: (v if v is not None else "") for k, v in flow.to_dict().items()}
            await redis.hset(f"buyflow:{user_id}", mapping=flow_dict)

        # clear matched ranges but keep method info
        if hasattr(flow, 'matched_ranges'):
            flow.matched_ranges = None
        flow.state = BuyState.ASK_AMOUNT
        # convert None values to empty string
        flow_dict = {k: (v if v is not None else "") for k, v in flow.to_dict().items()}
        await redis.hset(f"buyflow:{user_id}", mapping=flow_dict)
        # send a fresh message asking for amount (editing sometimes fails on edited/old messages)
        await _reply_or_edit(update, "لطفاً مقدار موجودی که میخواید انتقال بدید وارد کنید (فقط عدد).", edit=False)
        return

    # disabled method selected
    if data.startswith("buy:method_disabled:"):
        await _reply_or_edit(update, BUY_METHOD_DISABLED_MSG, edit=True)
        return

    # select method
    if data.startswith("buy:method:"):
        return await buy_method_callback(update, context)

    # confirm amount
    if data == "buy:confirm":
        return await buy_confirm_callback(update, context)
    
    if data.startswith("buy:choose:"):
        return await buy_choose_callback(update, context)

    # cancel flow
    if data == "buy:cancel":
        # clear flow and show main menu to user
        context.user_data.pop('buy_flow', None)
        await _reply_or_edit(update, "ادامه ی تراکنش لغو شد")
        try:
            # lazy import to avoid circular imports
            from bot.keyboards.main_menu import main_menu
            user_id = getattr(update.effective_user, 'id', None)
            if user_id:
                await _reply_or_edit(update, "انتخاب کنید", reply_markup=main_menu(user_id))
            else:
                await _reply_or_edit(update, "بازگشت به منوی اصلی.")
        except Exception:
            # fallback: if main_menu not available, just notify user
            await _reply_or_edit(update, "بازگشت به منوی اصلی.")
        return

    # verification / failure callbacks
    if data.startswith("buy:verify:"):
        return await buy_verify_callback(update, context)
    if data.startswith("buy:mark_failed:"):
        return await buy_mark_failed_callback(update, context)

    # listing callbacks
    if data.startswith("buy:list:"):
        return await buy_list_callback(update, context)
    if data == "buy:decline_listing":
        if flow:
            flow.state = BuyState.ASK_AMOUNT
            flow_dict = {k: (v if v is not None else "") for k, v in flow.to_dict().items()}
            await redis.hset(f"buyflow:{user_id}", mapping=flow_dict)

        await _reply_or_edit(update, "باشه، مقدار جدید رو وارد کن (فقط عدد).", edit=True)
        return

    # profile confirm
    if data == "buy:confirm_profile":
        return await profile_confirm_callback(update, context)

    # new transaction
    if data == "buy:new_transaction":
        return await buy_new_transaction_callback(update, context)

    # fallback
    await _reply_or_edit(update, "دستور ناشناخته.")



async def show_final_options(update, context, success=True):
    user_id = update.effective_user.id
    from bot.ui.buy_keyboards import final_options_keyboard
    if success:
        msg = "✅ تراکنش با موفقیت انجام شد."
    else:
        msg = "❌ تراکنش انجام نشد یا لغو شد."
    await update.message.reply_text(msg, reply_markup=final_options_keyboard(user_id))
    context.user_data.pop('buy_flow', None)




async def buy_new_transaction_callback(update, context):
    context.user_data.pop('buy_flow', None)
    await start_buy(update, context)
async def request_profile_confirmation(update, context):
    flow = context.user_data.get('buy_flow')
    user_id = update.effective_user.id
    from bot.services.backend_client import get_user_profile
    profile = await get_user_profile(user_id)
    from bot.ui.buy_messages import PROFILE_PROMPT_MSG, PROFILE_WARNING_MSG, PROFILE_CONFIRM_MSG, PROFILE_SUCCESS_MSG
    if not profile or not profile.get('full_name') or not profile.get('bank_account'):
        await update.message.reply_text(PROFILE_WARNING_MSG)
        await update.message.reply_text(PROFILE_PROMPT_MSG)
        flow.state = BuyState.AWAIT_PROFILE_INPUT
        return
    # Show profile and ask for confirmation
    msg = f"نام کامل: {profile.get('full_name', 'نامشخص')}\nشماره حساب: {profile.get('bank_account', 'نامشخص')}\n{PROFILE_CONFIRM_MSG}"
    from bot.ui.buy_keyboards import profile_confirm_keyboard
    await update.message.reply_text(msg, reply_markup=profile_confirm_keyboard())
    flow.state = BuyState.AWAIT_PROFILE_CONFIRM
    flow_dict = {k: (v if v is not None else "") for k, v in flow.to_dict().items()}
    await redis.hset(f"buyflow:{user_id}", mapping=flow_dict)

    
   

async def profile_input_handler(update, context):
    flow = context.user_data.get('buy_flow')
    if not flow or flow.state != BuyState.AWAIT_PROFILE_INPUT:
        return
    text = update.message.text.strip()
    # Expecting: "نام کامل - شماره حساب"
    parts = text.split('-')
    if len(parts) != 2:
        await update.message.reply_text("فرمت صحیح: نام کامل - شماره حساب")
        return
    full_name = parts[0].strip()
    bank_account = parts[1].strip()
    user_id = update.effective_user.id
    from bot.services.backend_client import update_user_profile
    await update_user_profile(user_id, {'full_name': full_name, 'bank_account': bank_account})
    flow.state = BuyState.AWAIT_PROFILE_CONFIRM
    flow_dict = {k: (v if v is not None else "") for k, v in flow.to_dict().items()}
    await redis.hset(f"buyflow:{user_id}", mapping=flow_dict)

    msg = f"نام کامل: {full_name}\nشماره حساب: {bank_account}\nآیا اطلاعات زیر را تأیید می‌کنید؟"
    from bot.ui.buy_keyboards import profile_confirm_keyboard
    await update.message.reply_text(msg, reply_markup=profile_confirm_keyboard())

async def profile_confirm_callback(update, context):
    flow = context.user_data.get('buy_flow')
    user_id = update.effective_user.id

    from bot.services.backend_client import get_user_profile, update_transaction_status

    profile = await get_user_profile(user_id)
    tx_id = getattr(flow, 'tx_id', None)
    await update_transaction_status(tx_id, 'success')
    from bot.ui.buy_messages import PROFILE_SUCCESS_MSG
    msg = f"{PROFILE_SUCCESS_MSG}\nشناسه تراکنش: {tx_id}\nنام: {profile.get('full_name', 'نامشخص')}\nشماره حساب: {profile.get('bank_account', 'نامشخص')}"
    await update.callback_query.edit_message_text(msg)
async def present_post_buy_options(update, context, tx_info):
    # tx_info: dict with transaction details
    msg = (
        f"جزئیات تراکنش:\n"
        f"قیمت خرید فوری: {tx_info.get('buy_now', 'نامشخص')}\n"
        f"قیمت پیشنهادی: {tx_info.get('bid', 'نامشخص')}\n"
        f"زمان باقی‌مانده: {tx_info.get('remaining_time', 'نامشخص')}\n"
        f"قرارداد: {tx_info.get('contract', 'نامشخص')}\n"
        f"مالکین: {tx_info.get('owners', 'نامشخص')}\n"
        f"بازی‌ها: {tx_info.get('games', 'نامشخص')}\n"
        f"گل‌ها: {tx_info.get('goals', 'نامشخص')}\n"
        f"مالیات: {tx_info.get('tax', 'نامشخص')}\n"
        f"شناسه پیگیری: {tx_info.get('tracking_id', 'نامشخص')}\n"
        "\nلطفاً وضعیت خرید را تایید کنید:"
    )
    from bot.ui.buy_keyboards import verify_or_fail_keyboard
    await update.message.reply_text(msg, reply_markup=verify_or_fail_keyboard(tx_info.get('tracking_id')))

async def buy_verify_callback(update, context):
    query = update.callback_query
    data = query.data
    flow = context.user_data.get('buy_flow')
    tx_id = data.split(":")[-1]
    player_id = getattr(flow, 'player_id', None)
    from bot.services.trade_control import verify_purchase
    verified = await verify_purchase(tx_id, player_id)
    from bot.services.backend_client import update_transaction_status
    if verified:
        await update_transaction_status(tx_id, 'success')
        await query.edit_message_text("✅ خرید با موفقیت انجام شد! لطفاً اطلاعات پروفایل را تایید کنید.")
        # Step 8: profile confirmation (not implemented here)
    else:
        await update_transaction_status(tx_id, 'failed')
        await query.edit_message_text("خرید انجام نشده، لطفاً چک کنید.")

async def buy_mark_failed_callback(update, context):
    query = update.callback_query
    data = query.data
    tx_id = data.split(":")[-1]
    from bot.services.backend_client import update_transaction_status
    await update_transaction_status(tx_id, 'failed')
    await query.edit_message_text("تراکنش لغو شد. می‌توانید دوباره تلاش کنید یا به منوی اصلی بازگردید.")
async def buy_list_callback(update, context):
    query = update.callback_query
    data = query.data
    flow = context.user_data.get('buy_flow')
    if not flow or flow.state != BuyState.PENDING:
        await query.answer()
        await query.edit_message_text("جریان خرید پیدا نشد یا در مرحله لیست نیست.")
        return
    player_id = data.split(":")[-1]
    user_id = query.from_user.id if query.from_user else 0
    payload = {
        'user_id': user_id,
        'direction': 'buy',
        'method_id': getattr(flow, 'method_id', None),
        'player_id': player_id,
        'amount_requested': getattr(flow, 'amount', None),
        'transfer_multiplier': getattr(flow, 'transfer_multiplier', 1),
        'status': 'pending',
        'meta': {}
    }
    from bot.services.buy_service import create_pending_transaction
    tx = await create_pending_transaction(payload)
    flow.tx_id = tx.get('id')
    flow_dict = {k: (v if v is not None else "") for k, v in flow.to_dict().items()}
    await redis.hset(f"buyflow:{user_id}", mapping=flow_dict)

    from bot.services.trade_control import emit_admin
    await emit_admin('transaction:pending', {'user_id': user_id, 'tx_id': flow.tx_id})
    await query.edit_message_text("در حال تلاش برای خرید و لیست … وضعیت را در همین پیام دریافت خواهید کرد.")

    async def buy_and_list_task():
        try:
            transfer_multiplier = getattr(flow, 'transfer_multiplier', 1)
            from bot.services.futbin import get_price_for_player
            buy_now_price = await get_price_for_player(player_id)
            max_buy_now = int((buy_now_price or 0) * transfer_multiplier)
            min_bid = int(max_buy_now * 0.95)
            from bot.services.trade_control import attempt_buy_and_list
            result = await attempt_buy_and_list(player_id, max_buy_now, min_bid)
            if result.get('captcha_required'):
                await emit_admin('transaction:captcha', {'tx_id': flow.tx_id, 'player_id': player_id})
                # Update transaction meta if needed
            elif result.get('success'):
                # Update backend transaction to buy_listed
                from bot.services.backend_client import update_transaction_status
                await update_transaction_status(flow.tx_id, 'buy_listed')
                # Optionally notify user
            else:
                await emit_admin('transaction:buy_failed', {'tx_id': flow.tx_id, 'player_id': player_id, 'error': result.get('error')})
        except Exception as e:
            await emit_admin('transaction:buy_failed', {'tx_id': flow.tx_id, 'player_id': player_id, 'error': str(e)})

    import asyncio
    asyncio.create_task(buy_and_list_task())
    
    
import asyncio 

async def present_transfer_player(update, context):
    flow = context.user_data.get('buy_flow')
    if not flow or not getattr(flow, 'matched_ranges', None):
    # use helper to reply (works for Message and CallbackQuery)
        await _reply_or_edit(update, "اطلاعات بازه کارت پیدا نشد. لطفاً دوباره مقدار را وارد کنید.")
        if flow:
            flow.state = BuyState.ASK_AMOUNT
            flow_dict = {k: (v if v is not None else "") for k, v in flow.to_dict().items()}
            await redis.hset(f"buyflow:{update.effective_user.id}", mapping=flow_dict)
        return


    # از اولین بازه‌ی مچ‌شده استفاده می‌کنیم
    range_ = flow.matched_ranges[0]
    primary_id = range_.get('primary_card_id')
    fallback_id = range_.get('fallback_card_id') or range_.get('secondary_card_id')  
    from bot.services.buy_service import get_player_card_info

    # اطلاعات کارت اول (primary)
    logging.error(f"present_transfer_player: primary_id={primary_id}")
    primary_info = await get_player_card_info(primary_id)
    if not primary_info:
        logging.warning(f"Player {primary_id} info is None")
        primary_info = {"player": {}, "buy_now_price": 0}
    transfer_multiplier = getattr(flow, 'transfer_multiplier', 1)

    if primary_info:
        p_player = primary_info['player']
        p_price = primary_info.get('buy_now_price', 0)
    else:
        p_player = {}
        p_price = 0

    p_transferable = int((p_price or 0) * transfer_multiplier)


    # اطلاعات کارت دوم (fallback) - اگر وجود داشته باشد
# اطلاعات کارت دوم (fallback) - اگر وجود داشته باشد
    fb_info = None
    f_player = {}
    f_price = 0
    f_transferable = 0
    if fallback_id:
        fb_info = await get_player_card_info(fallback_id)
        if not fb_info or not isinstance(fb_info, dict):
            # fallback not available — keep defaults
            logging.warning("present_transfer_player: fallback %s info is None", fallback_id)
        else:
            f_player = fb_info.get('player', {}) or {}
            f_price = fb_info.get('buy_now_price') or 0
            f_transferable = int((f_price or 0) * transfer_multiplier)


    # هدر با ایموجی
    header = "🤖✨ از دید هوش مصنوعی بهترین کارت برای انتقال شما این دو کارت هستن،کدوم یکی رو میخاید استفاده کنین؟  🤖✨"

    # قالب نمایش مشخصات هر کارت (بر اساس present_transfer_player خودت)
    def format_card_block(title, player, buy_now_price, transferable_amount):
        # اگر فیلدهای زیر نبودند، None-safe باش
        name = player.get('name', '')
        rating = player.get('rating', '')
        version = player.get('version', '')
        min_bn = player.get('min_buy_now_price')
        max_bn = player.get('max_buy_now_price')

        lines = [
            f"{title}\n \n",
            f"👤 نام: {name}",
            f"⭐ ریتینگ: {rating}",
            f"🏅 ورژن: {version}",
            f"💰 قیمت تقریبی خرید کارت: {buy_now_price if buy_now_price else '---'}",
            f"💸 مقدار تقریبی قابل انتقال ( {transferable_amount}"
        ]
        if min_bn or max_bn:
            lines.append(f"بازه BIN: {min_bn or '-'} — {max_bn or '-'}")
        return "\n".join(lines)

    msg_parts = [header, ""]
    msg_parts.append(format_card_block("— 🧑‍💻 بازیکن ۱", p_player, p_price, p_transferable))
    if fb_info:
        msg_parts.append("")
        msg_parts.append(format_card_block("— 🧑‍💻 بازیکن ۲", f_player, f_price, f_transferable))
    msg_parts.append("")
    msg_parts.append("☑️  یکی از گزینه‌ها را انتخاب کنید…  ☑️")
    msg = "\n".join(msg_parts)

    # مپ انتخاب‌ها را برای کال‌بک نگه می‌داریم
    flow.choice_map = {"1": primary_id}
    if fallback_id:
        flow.choice_map["2"] = fallback_id

    # ارسال پیام با کیبورد سه‌گزینه‌ای
    from bot.ui.buy_keyboards import choose_two_players_keyboard
    await _reply_or_edit(update, msg, reply_markup=choose_two_players_keyboard(has_second=bool(fallback_id)))


    # وضعیت را pending نگه داریم تا تایمر و انتخاب کار کند
    flow.state = BuyState.PENDING
    user_id = update.effective_user.id
    flow_dict = {k: (v if v is not None else "") for k, v in flow.to_dict().items()}
    await redis.hset(f"buyflow:{user_id}", mapping=flow_dict)
    
    # تایمر ۶۰ ثانیه‌ای مانند قبل
    async def timer():
        await asyncio.sleep(60)
        if flow.state == BuyState.PENDING:
            await _reply_or_edit(update, "⏳ زمان تمام شد، لطفاً مقدار را دوباره وارد کنید. ⏳")
            flow.state = BuyState.ASK_AMOUNT
            flow_dict = {k: (v if v is not None else "") for k, v in flow.to_dict().items()}
            await redis.hset(f"buyflow:{user_id}", mapping=flow_dict)


    asyncio.create_task(timer())



import inspect
import logging
from decimal import Decimal
from telegram import InlineKeyboardMarkup
from bot.ui.buy_messages import BUY_DISABLED_MSG, BUY_CHOOSE_METHOD_MSG, BUY_METHODS_INFO_MSG, BUY_METHODS_ERROR_MSG, BUY_METHOD_DISABLED_MSG
from bot.ui.buy_keyboards import method_list_keyboard
from bot.flows.buy_flows import BuyFlow, BuyState
from bot.services.buy_service import get_transfer_methods
from bot.services.backend_client import get_transaction_status
from bot.services.redis_client import redis_client as redis


# --- helper: reply or edit safely for both Message and CallbackQuery updates ---
async def _reply_or_edit(update, text=None, reply_markup=None, photo_url=None, edit=False):
    query = getattr(update, "callback_query", None)
    msg = getattr(update, "message", None)
    try:
        if query:
            # try to answer callback to remove loading state
            try:
                await query.answer()
            except Exception:
                pass

            if edit:
                try:
                    if photo_url:
                        await query.message.reply_photo(photo_url, caption=text or "", reply_markup=reply_markup)
                    else:
                        await query.edit_message_text(text or "", reply_markup=reply_markup)
                    return
                except Exception:
                    pass

            if photo_url:
                await query.message.reply_photo(photo_url, caption=text or "", reply_markup=reply_markup)
            else:
                await query.message.reply_text(text or "", reply_markup=reply_markup)
            return

        if msg:
            if photo_url:
                await msg.reply_photo(photo_url, caption=text or "", reply_markup=reply_markup)
            else:
                await msg.reply_text(text or "", reply_markup=reply_markup)
            return

        logging.warning("_reply_or_edit: no callback_query or message in update; text dropped: %s", text)

    except Exception as exc:
        logging.exception("Error in _reply_or_edit: %s", exc)
        if query:
            try:
                await query.answer(text="خطا در ارسال پیام. لطفاً بعداً تلاش کنید.", show_alert=False)
            except Exception:
                pass


async def start_buy(update, context):
    from bot.services.redis_client import get_redis
    from bot.utils.rate_limiter import rate_limiter
    user = getattr(update, 'effective_user', None)
    user_id = getattr(user, 'id', None)

    # Rate-limit check
    if user_id is not None and hasattr(rate_limiter, 'is_allowed'):
        try:
            allowed = rate_limiter.is_allowed(user_id)
        except Exception:
            allowed = True
        if not allowed:
            block_msg = "به دلیل درخواست‌های زیاد، استفاده شما به مدت 10 دقیقه موقتا مسدود شد."
            await _reply_or_edit(update, block_msg)
            try:
                from bot.services.trade_control import emit_admin
                await emit_admin('rate_limit:block', {'user_id': user_id})
            except Exception:
                logging.exception("emit_admin failed for rate_limit")
            return

    # get transaction status from backend
    try:
        status = await get_transaction_status()
    except Exception as e:
        logging.exception("Failed to get transaction status: %s", e)
        await _reply_or_edit(update, "خطا در بررسی وضعیت تراکنش‌ها. لطفاً بعداً تلاش کنید.")
        try:
            from bot.services.trade_control import emit_admin
            await emit_admin('buy:get_transaction_status_error', {'user_id': user_id, 'error': str(e)})
        except Exception:
            logging.exception("emit_admin failed for transaction status")
        return

    if status.get('buying_disabled'):
        await _reply_or_edit(update, BUY_DISABLED_MSG, edit=True)
        return

    # init flow and store in user_data
    flow = BuyFlow(state=BuyState.ASK_METHOD)
    context.user_data['buy_flow'] = flow
    redis=await get_redis()
    
    # convert None values to empty string
    flow_dict = {k: (v if v is not None else "") for k, v in flow.to_dict().items()}
    await redis.hset(f"buyflow:{user_id}", mapping=flow_dict)


    # send choose-method message then call show_transfer_methods
    await _reply_or_edit(update, BUY_CHOOSE_METHOD_MSG)
    await show_transfer_methods(update, context)


async def show_transfer_methods(update, context):
    try:
        methods = await get_transfer_methods()
    except Exception as e:
        logging.exception("Failed to fetch transfer methods: %s", e)
        await _reply_or_edit(update, BUY_METHODS_ERROR_MSG)
        try:
            from bot.services.trade_control import emit_admin
            await emit_admin('buy:get_transfer_methods_error', {'user_id': getattr(update.effective_user, 'id', None), 'error': str(e)})
        except Exception:
            logging.exception("emit_admin failed when reporting get_transfer_methods error")
        return

    if not methods:
        await _reply_or_edit(update, BUY_METHODS_ERROR_MSG)
        try:
            from bot.services.trade_control import emit_admin
            await emit_admin('buy:empty_methods', {'user_id': getattr(update.effective_user, 'id', None)})
        except Exception:
            logging.exception("emit_admin failed when reporting empty methods")
        return

    # Build keyboard and send
    try:
        kb = method_list_keyboard(methods)
    except Exception:
        kb = None
    await _reply_or_edit(update, BUY_METHODS_INFO_MSG, reply_markup=kb)



from bot.services.redis_client import get_redis

async def buy_method_callback(update, context):
    user_id = update.effective_user.id
    redis = await get_redis() 
    query = update.callback_query
    data = query.data
    flow = context.user_data.get('buy_flow')
    if not flow:
        await query.answer()
        await query.edit_message_text("جریان خرید پیدا نشد. لطفاً دوباره شروع کنید.")
        return
    if data.startswith("buy:method_disabled:"):
        await query.answer()
        await query.edit_message_text(BUY_METHOD_DISABLED_MSG)
        return
    if data.startswith("buy:method:"):
        method_id = data.split(":")[-1]
        from bot.services.buy_service import get_method
        method = await get_method(method_id)
        flow.method_id = method['id']
        flow.method_name = method['name']
        flow.transfer_multiplier = float(method['transfer_multiplier'])
        flow.state = BuyState.ASK_AMOUNT
        flow_dict = {k: (v if v is not None else "") for k, v in flow.to_dict().items()}
        await redis.hset(f"buyflow:{user_id}", mapping=flow_dict)
        await query.edit_message_text("لطفاً مقدار موجودی که میخواید انتقال بدید وارد کنید (فقط عدد).")
        return

async def buy_amount_handler(update, context):
    user_id = update.effective_user.id
    redis = await get_redis()  
    
    flow = context.user_data.get('buy_flow')
    if not flow or flow.state != BuyState.ASK_AMOUNT:
        return
    text = update.message.text.strip().replace(',', '')
    # Convert Persian digits to English
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    for p, e in zip(persian_digits, english_digits):
        text = text.replace(p, e)
    try:
        amount = int(text)
    except Exception:
        await update.message.reply_text("لطفاً مقدار را درست وارد کنید (مثلاً 150000).")
        return
    if amount <= 0:
        await update.message.reply_text("لطفاً مقدار را درست وارد کنید (مثلاً 150000).")
        return
    flow.amount = int(amount)
    flow.state = BuyState.AWAIT_CONFIRM
    flow_dict = {k: (v if v is not None else "") for k, v in flow.to_dict().items()}
    await redis.hset(f"buyflow:{user_id}", mapping=flow_dict)

    from bot.ui.buy_keyboards import confirm_amount_keyboard
    await update.message.reply_text(f"مقدار انتخاب شده: {amount}\nتایید می‌کنید؟", reply_markup=confirm_amount_keyboard())

async def buy_confirm_callback(update, context):
    redis = await get_redis()
    query = update.callback_query
    flow = context.user_data.get('buy_flow')
    if not flow or flow.state != BuyState.AWAIT_CONFIRM:
        await query.answer()
        await query.edit_message_text("زمان این کار تموم شده،با انتخاب menu شروع مجدد رو بزنین")
        return
    try:
        from bot.services.buy_service import get_card_ranges
        ranges = await get_card_ranges()
    except Exception:
        await query.edit_message_text("خطا در دریافت بازه‌های کارت. لطفاً بعداً تلاش کنید.")
        from bot.services.trade_control import emit_admin
        await emit_admin("خطا در دریافت بازه‌های کارت برای خرید")
        return
    amount = flow.amount
    matched = [r for r in ranges if r['min_value'] <= amount <= r['max_value']]
    if not matched:
        # Not in any range, suggest admin support
        from bot.ui.buy_keyboards import support_or_back_keyboard
        import os
        from dotenv import load_dotenv

        load_dotenv() 

        chat_link = os.getenv("ADMIN_CHAT_LINK", "@support")

        if chat_link.startswith("@"):
            chat_link = f"https://t.me/{chat_link[1:]}"
        msg = "به دلیل تشخیص هوش مصنوعی برای رعایت امنیت اکانت شما، این مقدار انتقال شما بهتر است توسط ادمین انجام بگیره."
        await query.edit_message_text(msg, reply_markup=support_or_back_keyboard(chat_link))
        return
    user_id = update.effective_user.id
    flow.matched_ranges = matched

    # تبدیل همه None، Decimal و لیست‌ها به مقادیر قابل ذخیره در Redis
    flow_dict = {}
    for k, v in flow.to_dict().items():
        if v is None:
            flow_dict[k] = ""
        elif isinstance(v, Decimal):
            flow_dict[k] = float(v)
        elif isinstance(v, list) or isinstance(v, dict):
            flow_dict[k] = str(v)  # تبدیل لیست و دیکشنری به string
        else:
            flow_dict[k] = v


    await redis.hset(f"buyflow:{user_id}", mapping=flow_dict)

    # نمایش دو کارت پیشنهادی و کیبورد انتخاب
    return await present_transfer_player(update, context)


async def buy_choose_callback(update, context):
    query = update.callback_query
    data = query.data
    flow = context.user_data.get('buy_flow')

    # باید در وضعیت PENDING باشیم (مثل قبل)
    if not flow or flow.state != BuyState.PENDING:
        await query.answer()
        await query.edit_message_text("جریان خرید پیدا نشد یا در مرحله انتخاب کارت نیست.")
        return

    choice_idx = data.split(":")[-1]  # "1" یا "2"
    choice_map = getattr(flow, 'choice_map', {})
    player_id = choice_map.get(choice_idx)
    if not player_id:
        await query.answer()
        await query.edit_message_text("انتخاب نامعتبر است.")
        return

    user_id = query.from_user.id if query.from_user else 0
    payload = {
        'user_id': user_id,
        'direction': 'buy',
        'method_id': getattr(flow, 'method_id', None),
        'player_id': player_id,
        'amount_requested': getattr(flow, 'amount', None),
        'transfer_multiplier': getattr(flow, 'transfer_multiplier', 1),
        'status': 'pending',
        'meta': {}
    }

    # همان کاری که در buy_list_callback انجام می‌دهی:
    from bot.services.buy_service import create_pending_transaction
    tx = await create_pending_transaction(payload)
    flow.tx_id = tx.get('id')
    flow_dict = {k: (v if v is not None else "") for k, v in flow.to_dict().items()}
    await redis.hset(f"buyflow:{user_id}", mapping=flow_dict)


    from bot.services.trade_control import emit_admin
    await emit_admin('transaction:pending', {'user_id': user_id, 'tx_id': flow.tx_id})

    await query.edit_message_text("در حال تلاش برای خرید و لیست … وضعیت را در همین پیام دریافت خواهید کرد.")