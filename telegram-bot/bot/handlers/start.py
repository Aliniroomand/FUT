from telegram import KeyboardButton

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.keyboards import main_menu
from bot.storage import is_logged_in
import requests
from bot.config import settings

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id if update.effective_user else None
    if user_id is not None and is_logged_in(user_id):
        # اگر لاگین است، منوی اصلی را نمایش بده
        await update.message.reply_text(
            "شما قبلاً وارد شده‌اید!",
            reply_markup=main_menu()
        )
        return
    # اگر لاگین نیست
    contact_keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("حله ذخیره کن!", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )
    await update.message.reply_text(
        "برای استفاده از ربات و امنیت اکانت شما باید ابتدا شماره موبایلتون ثبت و ذخیره بشه",
        reply_markup=contact_keyboard
    )
    context.user_data['auth_flow'] = 'wait_for_phone'
async def phone_contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # فقط زمانی که کاربر contact ارسال می‌کند
    if update.message and update.message.contact:
        phone = update.message.contact.phone_number
        context.user_data['phone'] = phone
        context.user_data['auth_flow'] = 'confirm_phone'
        confirm_keyboard = ReplyKeyboardMarkup([
            ["بله، شماره درست است"],
                ["خیر، وارد کردن شماره به این فرمت 09..."]
        ], resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            f"آیا این شماره صحیح است؟\n{phone}",
            reply_markup=confirm_keyboard
        )

async def confirm_phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('auth_flow') == 'confirm_phone':
        if update.message.text == "بله، شماره درست است":
            context.user_data['auth_flow'] = 'wait_for_email'
            await update.message.reply_text("لطفاً ایمیل خود را وارد کنید:")
            return
        if update.message.text == "خیر، وارد کردن شماره به این فرمت 09...":
            context.user_data['auth_flow'] = 'wait_for_phone_manual'
            await update.message.reply_text("شماره موبایل خود را به فرمت 09... وارد کنید:")
            return
    elif context.user_data.get('auth_flow') == 'wait_for_phone_manual':
        # کاربر شماره را دستی وارد می‌کند
        phone = update.message.text.strip()
        # اعتبارسنجی ساده شماره (مثلاً با 09 شروع شود و 11 رقم باشد)
        if not phone.isdigit() or not phone.startswith('09') or len(phone) != 11:
            await update.message.reply_text("شماره وارد شده معتبر نیست. لطفاً به صورت 09... وارد کنید:")
            return
        context.user_data['phone'] = phone
        context.user_data['auth_flow'] = 'confirm_phone'
        confirm_keyboard = ReplyKeyboardMarkup([
            ["بله، شماره درست است"],
            ["خیر، وارد کردن شماره به این فرمت 09..."]
        ], resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            f"آیا این شماره صحیح است؟\n{phone}",
            reply_markup=confirm_keyboard
        )
    elif context.user_data.get('auth_flow') == 'wait_for_email':
        # کاربر ایمیل را وارد می‌کند
        email = update.message.text.strip()
        phone = context.user_data.get('phone')
        if not email or '@' not in email:
            await update.message.reply_text("ایمیل وارد شده معتبر نیست. لطفاً مجدداً وارد کنید:")
            return
        # ارسال شماره و ایمیل به بک‌اند
        try:
            api_url = f"{settings.backend_url}/auth/register"
            payload = {"phone_number": phone, "email": email, "password": str(phone)[-6:]}
            session = requests.Session()
            session.trust_env = False
            # prefer explicit proxies if provided in settings
            proxies = None
            if settings.http_proxy or settings.https_proxy:
                proxies = {}
                if settings.http_proxy:
                    proxies['http'] = settings.http_proxy
                if settings.https_proxy:
                    proxies['https'] = settings.https_proxy
            response = session.post(api_url, json=payload, timeout=10, proxies=proxies)
            if response.status_code == 200:
                data = response.json()
                context.user_data['access_token'] = data.get('access_token')
                context.user_data['refresh_token'] = data.get('refresh_token')
                context.user_data['is_logged_in'] = True
                context.user_data['auth_flow'] = None
                await update.message.reply_text("ثبت‌نام/ورود با موفقیت انجام شد!",
                                              reply_markup=main_menu())
            else:
                # اگر کاربر قبلاً ثبت‌نام کرده باشد، تلاش برای لاگین
                if response.status_code == 400 and ('قبلا ثبت شده' in response.text or 'قبلا ثبت' in response.text):
                    login_url = f"{settings.backend_url}/auth/login"
                    login_payload = {"email": email, "password": str(phone)[-6:]}
                    login_resp = session.post(login_url, json=login_payload, timeout=10, proxies=proxies)
                    if login_resp.status_code == 200:
                        data = login_resp.json()
                        context.user_data['access_token'] = data.get('access_token')
                        context.user_data['refresh_token'] = data.get('refresh_token')
                        context.user_data['is_logged_in'] = True
                        context.user_data['auth_flow'] = None
                        await update.message.reply_text("ورود با موفقیت انجام شد!",
                                                      reply_markup=main_menu())
                    else:
                        await update.message.reply_text("خطا در ورود. لطفاً بعداً تلاش کنید.")
                else:
                    await update.message.reply_text("خطا در ثبت‌نام. لطفاً بعداً تلاش کنید.")
        except Exception as e:
            await update.message.reply_text("خطا در ارتباط با سرور. لطفاً بعداً تلاش کنید.")
        return
    else:
        await update.message.reply_text(
            "به اولین مرجع مدیریت ادمین + هوش مصنوعی سکه های  FUT خوش آمدید!",
            reply_markup=main_menu()
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "دستورات موجود:\n/start - شروع\n/help - راهنما\n/health - بررسی وضعیت ربات"
    )

async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Bot is alive")




