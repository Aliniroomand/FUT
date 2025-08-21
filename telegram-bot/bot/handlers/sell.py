from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.services.futbin import get_player_price, get_player_image
from bot.services.ws_client import emit_admin
from bot.utils.rate_limiter import check_user_limit
from bot.proxy import requests_get
import requests
from bot.config import settings
import asyncio
import logging
import os


logger = logging.getLogger(__name__)
admin_username = os.getenv("ADMIN_USERNAME")


def sync_get(url: str, timeout: int = 5, user_id: int | None = None):
    """Use configured requests session and return response or None on error.
    Also schedules an admin emit on exception for diagnostics.
    """
    try:
        resp = requests_get(url, timeout=timeout)
        return resp
    except Exception as e:
        logger.exception("sync GET failed %s", url)
        # try to notify admin panel asynchronously
        try:
            if user_id is not None:
                asyncio.get_event_loop().create_task(emit_admin('error:backend_request_exception', {'user_id': user_id, 'url': url, 'error': str(e)}))
        except Exception:
            logger.exception('failed to schedule emit_admin')
        return None

# We'll use user_data['sell_flow'] to keep state for the sell flow.

async def handle_sell_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # support being called from a CallbackQuery or a Message
    query = getattr(update, 'callback_query', None)
    if query:
        await query.answer()
        target = query.message
    else:
        target = update.message

    user_id = update.effective_user.id
    # rate limit per user
    if not check_user_limit(user_id):
        await target.reply_text(
            "به دلیل ارسال درخواست‌های زیاد، دسترسی شما برای مدتی محدود شد. لطفاً بعداً تلاش کنید."
        )
        await emit_admin('alert:rate_limit', {'user_id': user_id})
        return

    # 1. check global status from backend
    r = sync_get(f"{settings.backend_url}/transaction-status", timeout=5)
    if r is None:
        await target.reply_text("خطا در دریافت وضعیت سرور. لطفاً بعداً تلاش کنید.")
        return
    if r.status_code == 200:
        data = r.json()
        buying_disabled = data.get('buying_disabled', 0)
        selling_disabled = data.get('selling_disabled', 0)
    else:
        body = ''
        try:
            body = r.text
        except Exception:
            body = '<unreadable>'
        logger.warning("backend /transaction-status returned %s for user=%s url=%s", r.status_code, user_id, r.url)
        try:
            asyncio.get_event_loop().create_task(emit_admin('error:backend_status', {'user_id': user_id, 'status': r.status_code, 'url': str(r.url), 'response_text': (body or '')[:2000]}))
        except Exception:
            logger.exception('failed to schedule emit_admin')
        await target.reply_text("خطا در دریافت وضعیت تراکنش‌ها. لطفاً بعداً تلاش کنید.")
        return

    if selling_disabled:
        await target.reply_text(
            "*⛔️ در حال حاضر سیستم خرید سکه ما فعال نیست.⛔️*\n\n"
            "لطفاً برای اطلاع از وضعیت بعدی، به ما مراجعه کنید یا با پشتیبانی تماس بگیرید.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 چت با پشتیبانی", url=f"https://t.me/{settings.admin_username}")]
        ])
    )
        return

    # 2. get transfer methods
    r = sync_get(f"{settings.backend_url}/transfer-methods", timeout=5, user_id=user_id)
    if r and r.status_code == 200:
        try:
            methods = r.json()
        except Exception:
            methods = []
    else:
        methods = []
        if r is not None:
            body = ''
            try:
                body = r.text
            except Exception:
                body = '<unreadable>'
            logger.warning('transfer-methods returned %s url=%s', getattr(r, 'status_code', None), getattr(r, 'url', None))
            try:
                asyncio.get_event_loop().create_task(emit_admin('error:transfer_methods', {'user_id': user_id, 'status': getattr(r, 'status_code', None), 'url': str(getattr(r, 'url', '')), 'response_text': (body or '')[:2000]}))
            except Exception:
                logger.exception('failed to schedule emit_admin')

    if not methods:
        await target.reply_text("هیچ روش انتقال فعالی در دسترس نیست. لطفا بعدا تلاش کنید.")
        return

    # show only active methods as buttons, show inactive as disabled labels
    buttons = []
    for m in methods:
        name = m.get("name", "نامشخص")
        method_id = m.get("id")

        if m.get("is_active"): 
            label = f"{name} ✅ فعال"
            buttons.append([
                InlineKeyboardButton(label, callback_data=f"sell:method:{method_id}")
            ])
        else:  
            label = f"{name} ❌ غیرفعال"
            buttons.append([
                InlineKeyboardButton(label, callback_data="sell:method:disabled")
            ])
    await target.reply_text(
        "<b>❓ کدام روش انتقال را می‌خواهید استفاده کنید؟</b>\n\n"
        "🔹 اگر متدی غیرفعال باشد نمایش داده می‌شود  اما <u>انتخاب‌شدنی نیستند</u>.\n\n"
        "🤖 متدهای فعال بر اساس <b>تشخیص هوش مصنوعی</b> و <b>ادمین</b> انتخاب شده‌اند، "
        "تا با توجه به وضعیت لحظه‌ای مارکت، <u><b>کمترین ریسک</b></u> را داشته باشند.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    context.user_data['sell_flow'] = {'step': 'choose_method'}


async def sell_callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data or ''
    user_id = query.from_user.id

    flow = context.user_data.get('sell_flow') or {}

    # handle method selection
    if data.startswith('sell:method:') and flow.get('step') == 'choose_method':
        _, _, method_id = data.split(':')
        if method_id == 'disabled':
            await query.edit_message_text('این روش غیرفعال است. لطفاً روش دیگری انتخاب کنید.')
            return
        # save method and ask amount
        context.user_data['sell_flow']['method_id'] = int(method_id)
        context.user_data['sell_flow']['step'] = 'ask_amount'
        await query.edit_message_text(
    "*💰 لطفاً مقدار سکه‌ای که می‌خواهید بفروشید را وارد کنید:* \n\n"
    "📌 فقط عدد وارد کنید.\n\n"
    "مثال: برای *100,کا* سکه  فقط بنویسید `100`",
    parse_mode="HTML"
)
        return

    await query.edit_message_text('عملیات نامشخص است. لطفاً دوباره تلاش کنید.')


async def sell_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    flow = context.user_data.get('sell_flow')
    if not flow:
        # not in sell flow
        return

    step = flow.get('step')
    text = update.message.text.strip()

    if step == 'ask_amount':
        if not text.isdigit():
            await update.message.reply_text('مقدار وارد شده معتبر نیست. لطفاً فقط عدد وارد کنید:')
            return
        amount = int(text)
        context.user_data['sell_flow']['amount'] = amount

        # fetch ranges from backend
        r = requests_get(f"{settings.backend_url}/card-range", timeout=5)
        if r and getattr(r, 'status_code', None) == 200:
            try:
                ranges = r.json()
            except Exception:
                ranges = []
        else:
            ranges = []

        matched = None
        for rng in ranges:
            if rng.get('min_amount') <= amount <= rng.get('max_amount'):
                matched = rng
                break

        if not matched:
            await update.message.reply_text(
                'به دلیل تشخیص هوش مصنوعی این مقدار در بازه ی خطرناک قرار گرفته، \nبرای رعایت امنیت اکانت شما، این مقدار انتقال بهتر است توسط ادمین انجام بگیرد.\nبرای ارتباط با پشتیبانی کلیک کنید.'
            )
            context.user_data.pop('sell_flow', None)
            return

        # get player cards
        primary_id = matched.get('primary_player_id')
        secondary_id = matched.get('secondary_player_id')
        # load player info from backend
        r1 = requests_get(f"{settings.backend_url}/player_card/{primary_id}")
        if r1 and getattr(r1, 'status_code', None) == 200:
            try:
                p1 = r1.json()
            except Exception:
                p1 = {}
        else:
            p1 = {}
        r2 = requests_get(f"{settings.backend_url}/player_card/{secondary_id}")
        if r2 and getattr(r2, 'status_code', None) == 200:
            try:
                p2 = r2.json()
            except Exception:
                p2 = {}
        else:
            p2 = {}

        # fetch futbin info
        buy1 = await get_player_price(primary_id)
        buy2 = await get_player_price(secondary_id)
        img1 = await get_player_image(primary_id)
        img2 = await get_player_image(secondary_id)

        method_id = context.user_data['sell_flow']['method_id']
        # get method multiplier from backend
        rm = requests_get(f"{settings.backend_url}/transfer-methods/{method_id}")
        if rm and getattr(rm, 'status_code', None) == 200:
            try:
                method = rm.json()
            except Exception:
                method = {}
        else:
            method = {}
        multiplier = method.get('transfer_multiplier', 1)

        # compute transferable amounts
        transferable1 = (buy1 or 0) * multiplier
        transferable2 = (buy2 or 0) * multiplier

        # store details
        context.user_data['sell_flow'].update({
            'matched_range': matched,
            'primary': p1,
            'secondary': p2,
            'buy1': buy1,
            'buy2': buy2,
            'img1': img1,
            'img2': img2,
            'transferable1': transferable1,
            'transferable2': transferable2,
            'step': 'show_options'
        })

        # show choices
        btns = [
            [InlineKeyboardButton('لیست کن', callback_data='sell:do_list')],
            [InlineKeyboardButton('نه نمی‌خوام', callback_data='sell:do_cancel')],
        ]

        msg = f"بازیکن: {p1.get('player_name', 'نامشخص')}\nقیمت تقریبی Buy Now: {buy1 or 'نامشخص'}\nمیزان قابل انتقال تقریبی: {transferable1}\n"
        await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(btns))

    elif step == 'show_options':
        # ignore free text while options are showing
        return

    else:
        return
