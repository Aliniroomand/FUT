from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import httpx
from bot.config import settings
from bot.storage import save_token
import logging

logger = logging.getLogger(__name__)

# Simple text-based auth flow using user_data to track steps

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text == "ثبت‌نام":
        context.user_data['auth_flow'] = 'register_name'
        await update.message.reply_text("لطفاً نام خود را وارد کنید:")


async def register_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('auth_flow') != 'register_name':
        return

    name = update.message.text if update.message else ''
    user_id = update.effective_user.id if update.effective_user else None
    payload = {"name": name, "telegram_id": user_id}

    async with httpx.AsyncClient(trust_env=True) as client:
        try:
            r = await client.post(f"{settings.backend_url}/register", json=payload, timeout=10)
            if r.status_code == 201:
                login_keyboard = ReplyKeyboardMarkup([["ورود"]], resize_keyboard=True, one_time_keyboard=True)
                await update.message.reply_text("ثبت‌نام موفق بود! حالا می‌توانید وارد شوید.", reply_markup=login_keyboard)
            else:
                detail = r.json().get('detail') if r.headers.get('content-type','').startswith('application/json') else r.text
                await update.message.reply_text(f"خطا: {detail}")
        except Exception as e:
            logger.exception("Error while registering user")
            await update.message.reply_text("خطا در ارتباط با سرور. لطفاً بعداً تلاش کنید.")
        finally:
            context.user_data.pop('auth_flow', None)


async def login_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text == "ورود":
        context.user_data['auth_flow'] = 'login_username'
        await update.message.reply_text("لطفاً شماره یا نام کاربری خود را وارد کنید:")


async def login_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('auth_flow') != 'login_username':
        return

    username = update.message.text if update.message else ''
    payload = {"username": username}
    async with httpx.AsyncClient(trust_env=True) as client:
        try:
            r = await client.post(f"{settings.backend_url}/login", json=payload, timeout=10)
            if r.status_code == 200:
                data = r.json()
                token = data.get("access_token")
                if token and update.effective_user:
                    save_token(update.effective_user.id, token)
                    # send main menu (use reply keyboard removal by sending empty reply_markup)
                    await update.message.reply_text("ورود موفق بود!", reply_markup=ReplyKeyboardMarkup([["منو"]], resize_keyboard=True))
                else:
                    await update.message.reply_text("خطا: توکن دریافت نشد.")
            else:
                await update.message.reply_text("نام کاربری یا رمز اشتباه است.")
        except Exception:
            logger.exception("Error while logging in")
            await update.message.reply_text("خطا در ارتباط با سرور. لطفاً بعداً تلاش کنید.")
        finally:
            context.user_data.pop('auth_flow', None)
