from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import httpx
from bot.config import settings
from bot.storage import save_token
import logging

logger = logging.getLogger(__name__)


async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass


async def register_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # اگر در مرحله دریافت ایمیل هستیم
    if context.user_data.get('auth_flow') == 'wait_for_email':
        email = update.message.text if update.message else ''
        phone = context.user_data.get('phone')
        user_id = update.effective_user.id if update.effective_user else None
        # backend expects phone_number, email and password
        password = str(phone)[-6:] if phone else ''
        payload = {"phone_number": phone, "email": email, "password": password, "telegram_id": user_id}
        async with httpx.AsyncClient(trust_env=False) as client:
            try:
                r = await client.post(f"{settings.backend_url}/auth/register", json=payload, timeout=10)
                # backend returns 200 with token on success
                if r.status_code == 200:
                    login_keyboard = ReplyKeyboardMarkup([["ورود"]], resize_keyboard=True, one_time_keyboard=True)
                    await update.message.reply_text("ثبت‌نام موفق بود! حالا می‌توانید وارد شوید.", reply_markup=login_keyboard)
                else:
                    # extract detail safely
                    try:
                        detail = r.json().get('detail')
                    except Exception:
                        detail = r.text
                    await update.message.reply_text(f"خطا: {detail}")
            except Exception:
                logger.exception("Error while registering user")
                await update.message.reply_text("خطا در ارتباط با سرور. لطفاً بعداً تلاش کنید.")
            finally:
                context.user_data.pop('auth_flow', None)


async def login_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass


async def login_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # اگر در مرحله دریافت ایمیل برای ورود هستیم
    if context.user_data.get('auth_flow') == 'wait_for_email':
        email = update.message.text if update.message else ''
        phone = context.user_data.get('phone')
        # backend expects email and password for login
        password = str(phone)[-6:] if phone else ''
        payload = {"email": email, "password": password}
        async with httpx.AsyncClient(trust_env=False) as client:
            try:
                r = await client.post(f"{settings.backend_url}/auth/login", json=payload, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    token = data.get("access_token")
                    if token and update.effective_user:
                        save_token(update.effective_user.id, token)
                        await update.message.reply_text("ورود موفق بود!", reply_markup=ReplyKeyboardMarkup([["منو"]], resize_keyboard=True))
                    else:
                        await update.message.reply_text("خطا: توکن دریافت نشد.")
                else:
                    await update.message.reply_text("شماره یا ایمیل اشتباه است.")
            except Exception:
                logger.exception("Error while logging in")
                await update.message.reply_text("خطا در ارتباط با سرور. لطفاً بعداً تلاش کنید.")
            finally:
                context.user_data.pop('auth_flow', None)
