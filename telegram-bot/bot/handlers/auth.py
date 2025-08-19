from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import httpx
from bot.config import settings
from bot.storage import save_token, delete_token, token_exists
from bot.keyboards.main_menu import main_menu
from bot.keyboards.auth import auth_menu
import logging

logger = logging.getLogger(__name__)

MAIN_MENU = ReplyKeyboardMarkup([["🏠 منو"]], resize_keyboard=True)
CANCEL_KB = ReplyKeyboardMarkup([["❌ لغو"]], resize_keyboard=True, one_time_keyboard=True)

# ======== ثبت‌نام ========
async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text("🆕 ثبت‌نام\n\n📱 لطفاً شماره موبایل خود را وارد کنید:\n ⚠️ 09...  ⚠️")
    else:
        await update.message.reply_text("🆕 ثبت‌نام\n\n📱 لطفاً شماره موبایل خود را وارد کنید:\n⚠️ 09...  ⚠️", reply_markup=CANCEL_KB)
    context.user_data['auth_flow'] = 'wait_for_phone_register'

async def login_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text("🔐 ورود\n\n📱 لطفاً شماره موبایل خود را وارد کنید:\n   ⚠️ 09...  ⚠️ ")
    else:
        await update.message.reply_text("🔐 ورود\n\n📱 لطفاً شماره موبایل خود را وارد کنید:\n ⚠️ 09...  ⚠️ ", reply_markup=CANCEL_KB)
    context.user_data['auth_flow'] = 'wait_for_phone_login'

# ======== لاگ‌اوت ========
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    delete_token(user_id)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "✅ شما با موفقیت از حساب خود خارج شدید.",
        reply_markup=main_menu(user_id)
    )

# ======== هندلر متن برای مراحل auth ========
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    flow = context.user_data.get('auth_flow')

    if text == "❌ لغو":
        context.user_data.pop('auth_flow', None)
        await update.message.reply_text("🛑 عملیات لغو شد.", reply_markup=MAIN_MENU)
        return

    # ======== ثبت‌نام ========
    if flow == 'wait_for_phone_register':
        context.user_data['phone_number'] = text
        context.user_data['auth_flow'] = 'wait_for_email_register'
        await update.message.reply_text("📧 لطفاً ایمیل خود را وارد کنید:", reply_markup=CANCEL_KB)

    elif flow == 'wait_for_email_register':
        context.user_data['email'] = text
        context.user_data['auth_flow'] = 'wait_for_password_register'
        await update.message.reply_text("🔑 لطفاً رمز عبور خود را وارد کنید:\n ⚠️رمز عبور باید حداقل 6 رقم باشد", reply_markup=CANCEL_KB)

    elif flow == 'wait_for_password_register':
        phone = context.user_data.get('phone_number')
        email = context.user_data.get('email')
        password = text
        payload = {"phone_number": phone, "email": email, "password": password}

        async with httpx.AsyncClient(trust_env=False) as client:
            try:
                r = await client.post(f"{settings.backend_url}/auth/register", json=payload, timeout=10)
                if r.status_code == 200:
                    await update.message.reply_text(
                        "✅ ثبت‌نام موفق بود! حالا می‌توانید وارد شوید.",
                        reply_markup=ReplyKeyboardMarkup([["🔐 ورود"]], resize_keyboard=True)
                    )
                else:
                    detail = r.json().get('detail', r.text)
                    await update.message.reply_text(f"❌ خطا: {detail}")
            except Exception:
                logger.exception("Error while registering user")
                await update.message.reply_text("⚠️ خطا در ارتباط با سرور. لطفاً بعداً تلاش کنید.")
            finally:
                context.user_data.pop('auth_flow', None)

    # ======== ورود ========
    elif flow == 'wait_for_phone_login':
        context.user_data['phone_number'] = text
        context.user_data['auth_flow'] = 'wait_for_email_login'
        await update.message.reply_text("📧 لطفاً ایمیل خود را وارد کنید:", reply_markup=CANCEL_KB)

    elif flow == 'wait_for_email_login':
        context.user_data['email'] = text
        context.user_data['auth_flow'] = 'wait_for_password_login'
        await update.message.reply_text("🔑 لطفاً رمز عبور خود را وارد کنید:\n ⚠️رمز عبور باید حداقل 6 رقم باشد ", reply_markup=CANCEL_KB)

    elif flow == 'wait_for_password_login':
        phone = context.user_data.get('phone_number')
        email = context.user_data.get('email')
        password = text
        payload = {"phone": phone, "email": email, "password": password}

        async with httpx.AsyncClient(trust_env=False) as client:
            try:
                r = await client.post(f"{settings.backend_url}/auth/login", json=payload, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    token = data.get("access_token")
                    user_id = update.effective_user.id
                    if token and user_id:
                        save_token(user_id, token)
                        await update.message.reply_text(
                            "✅ ورود موفق بود!",
                            reply_markup=main_menu(user_id)
                        )
                    else:
                        await update.message.reply_text("❌ خطا: توکن دریافت نشد.")
                else:
                    detail = r.json().get('detail', r.text)
                    await update.message.reply_text(f"❌ خطا: {detail}")
            except Exception:
                logger.exception("Error while logging in")
                await update.message.reply_text("⚠️ خطا در ارتباط با سرور. لطفاً بعداً تلاش کنید.")
            finally:
                context.user_data.pop('auth_flow', None)
