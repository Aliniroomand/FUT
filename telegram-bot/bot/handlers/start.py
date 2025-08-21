from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.keyboards.main_menu import main_menu
from bot.keyboards.persistent import persistent_menu
from bot.storage import token_exists
from bot.config import settings
import httpx
from decimal import Decimal
from datetime import datetime
import logging
import re
import json
import jdatetime


logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query if hasattr(update, 'callback_query') else None
    target = None
    if query and query.message:
        target = query.message
        await query.answer()
    elif update.message:
        target = update.message
    else:
        return

    user_id = update.effective_user.id if update.effective_user else None
    name = update.effective_user.first_name if update.effective_user else ""

    # show welcome only once per user session unless forced
    if context.user_data.get('seen_welcome'):
        # show main menu directly
        await target.reply_text(
            f"✅ خوش اومدی {name}!\n\nچه کاری میتونم برات انجام بدم؟:",
            reply_markup=main_menu(user_id or 0)
        )
        return



    # persistent menu (near input) will be attached too
    persistent_kb = persistent_menu()

    await target.reply_text(
        f"✨ سلام {name}! خوبی؟ \n\n"
        "به اولین سامانه مدیریت سکه ( ادمین + هوش مصنوعی ) خوش اومدی💎\n\n"
    )

    # send persistent menu as a second message (it stays near input)
    await target.reply_text(" از منوی زیر  انتخاب کن که چه کاری برات انجام بدم؟ :", reply_markup=persistent_kb)

    context.user_data['seen_welcome'] = True

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "ℹ️ راهنما:\n\n"
        "🟢 /start - شروع و نمایش منو\n"
        "🟢 /help - نمایش همین راهنما\n"
        "🟢 /health - بررسی وضعیت ربات"
    )

async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ ربات فعال است و مشکلی ندارد.")

async def web_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text == "🌐 ورود به وبسایت":
        url = settings.frontend_url

        # اگر localhost بود، چون تلگرام بلاک می‌کنه، فقط متن بده
        if url.startswith("http://localhost") or url.startswith("http://127.0.0.1"):
            await update.message.reply_text(
                f"برای باز کردن وبسایت آدرس زیر را در مرورگر خود باز کنید:\n{url}",
                disable_web_page_preview=False  # برای localhost preview نمیاد
            )
            return

        # روش پیشنهادی: هم preview هم دکمه
        btn = InlineKeyboardButton("🔗 باز کردن وبسایت", url=url)
        markup = InlineKeyboardMarkup([[btn]])
        await update.message.reply_text(
            f"🌐 برای باز کردن وبسایت روی لینک زیر کلیک کنید:\n{url}",
            reply_markup=markup,
            disable_web_page_preview=False  # اینجا preview میاد
        )

# show online price
async def price_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # call backend /prices/latest and show buy/sell prices in a styled message
    if not (update.message and update.message.text == "💹 استعلام قیمت"):
        return

    url = f"{settings.backend_url}/prices/latest"
    try:
        # Prefer a direct connection (no proxy/env) for local backends to avoid proxy-caused 502s
        async with httpx.AsyncClient(trust_env=False) as client:
            r = await client.get(url, timeout=5)
    except Exception as e:
        logger.exception("Direct HTTP request failed for prices/latest (trust_env=False)")
        # fallback to honoring environment (in case a proxy is required)
        try:
            async with httpx.AsyncClient(trust_env=True) as client:
                r = await client.get(url, timeout=5)
        except Exception:
            logger.exception("Fallback HTTP request failed for prices/latest (trust_env=True)")
            await update.message.reply_text("⚠️ خطا در برقراری ارتباط با سرور قیمت‌ها. لطفاً بعداً تلاش کنید.")
            return
    response_to_use = r
    if r.status_code != 200:
        logger.error("prices/latest returned status %s for URL %s: %s", r.status_code, r.url, r.text[:1000])
        # diagnostic: try again without proxy/env to see if proxy causes 502
        try:
            async with httpx.AsyncClient(trust_env=False) as client2:
                r2 = await client2.get(url, timeout=5)
                logger.info("Diagnostic try (trust_env=False) returned status %s for URL %s: %s", r2.status_code, r2.url, r2.text[:1000])
                if r2.status_code == 200:
                    # try to parse diagnostic response immediately and use it
                    response_to_use = r2
                    try:
                        data = r2.json()
                        logger.info("Diagnostic response parsed as JSON and will be used")
                    except Exception as e_json:
                        raw2 = r2.text or ''
                        logger.warning("Diagnostic response JSON parse failed: %s; raw repr: %r", e_json, raw2[:2000])
                        # try json.loads on cleaned text
                        cleaned2 = raw2.strip()
                        if cleaned2.startswith('\ufeff'):
                            cleaned2 = cleaned2.lstrip('\ufeff')
                        try:
                            data = json.loads(cleaned2)
                            logger.info("Diagnostic response json.loads succeeded and will be used")
                        except Exception as e2:
                            logger.warning("Diagnostic json.loads also failed: %s", e2)
                            # leave data as None -> will fallback to regex on response_to_use
                else:
                    await update.message.reply_text("⚠️ خطا در دریافت قیمت‌ها از سرور. لطفاً بعداً تلاش کنید.")
                    return
        except Exception:
            logger.exception("Diagnostic request without env-proxy failed")
            await update.message.reply_text("⚠️ خطا در برقراری ارتباط با سرور قیمت‌ها. لطفاً بعداً تلاش کنید.")
            return

    # parse JSON robustly from the selected response; fallback to text regex parsing if needed
    logger.info("Using response from %s (status %s) for parsing", getattr(response_to_use, 'url', 'unknown'), getattr(response_to_use, 'status_code', 'unknown'))
    raw = (response_to_use.text or '')
    # try json.loads directly on text (more explicit and consistent)
    try:
        cleaned = raw.strip()
        if cleaned.startswith('\ufeff'):
            cleaned = cleaned.lstrip('\ufeff')
        data = json.loads(cleaned)
    except Exception as e:
        logger.warning("json.loads failed for prices/latest response: %s; raw repr: %r", e, raw[:2000])
        text = raw
        # attempt to find floats in the text like 'buy_price: 123.45' or numbers
        m_buy = re.search(r"buy[_\- ]?price\D*([0-9.,]+)", text, flags=re.I)
        m_sell = re.search(r"sell[_\- ]?price\D*([0-9.,]+)", text, flags=re.I)
        if m_buy or m_sell:
            data = {}
            if m_buy:
                data['buy_price'] = m_buy.group(1)
            if m_sell:
                data['sell_price'] = m_sell.group(1)
        else:
            logger.error("Could not extract buy/sell from text response: %s", text[:300])
            await update.message.reply_text("⚠️ خطا در تحلیل پاسخ سرور. لطفاً بعداً تلاش کنید.")
            return

    def num_normalize(v):
        try:
            if v is None:
                return Decimal(0)
            s = str(v).strip()
            s = s.replace(',', '')
            return Decimal(s)
        except Exception:
            return Decimal(0)

    buy = num_normalize(data.get('buy_price'))
    sell = num_normalize(data.get('sell_price'))

    # try to read timestamp from backend response (common keys)
    ts = None
    for key in ('updated_at', 'timestamp', 'updated', 'created_at'):
        if key in data and data.get(key):
            ts = data.get(key)
            break

    if ts:
        # try parse ISO formats, handle 'Z'
        try:
            if isinstance(ts, (int, float)):
                dt = datetime.fromtimestamp(float(ts)).astimezone()
            else:
                s = str(ts)
                if s.endswith('Z'):
                    s = s.replace('Z', '+00:00')
                dt = datetime.fromisoformat(s).astimezone()
        except Exception:
            dt = datetime.now().astimezone()
    else:
        dt = datetime.now().astimezone()

    jdt = jdatetime.datetime.fromgregorian(datetime=dt)
    time_str = jdt.strftime('%Y/%m/%d %H:%M:%S')

    text = (
        f"� <b>استعلام قیمت ( به ازای هر 100 کا) </b> 💱\n\n"
        f"� <b>قیمت خرید:</b> <code>{buy:,.0f}</code> تومان\n"
        f"� <b>قیمت فروش:</b> <code>{sell:,.0f}</code> تومان\n\n"
        f"🕒 <b>زمان دریافت :</b> {time_str}\n\n"
        "ℹ️ با زدن این کلید، آخرین قیمتِ ثبت‌شده در سرور دریافت می‌شود."
    )

    # send as formatted HTML message
    await update.message.reply_text(text, parse_mode='HTML', disable_web_page_preview=True)
