from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bot.storage import is_logged_in, get_token
from bot.config import settings
from bot.utils.decorators import login_required
import httpx
import logging

logger = logging.getLogger(__name__)

main_menu_keyboard = ReplyKeyboardMarkup(
    [["مشاهده تراکنش‌ها", "فروش سکه", "پروفایل"]],
    resize_keyboard=True
)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id if update.effective_user else None
    if user_id and is_logged_in(user_id):
        await update.message.reply_text("به منوی اصلی خوش آمدید!", reply_markup=main_menu_keyboard)
    else:
        await update.message.reply_text("لطفاً ابتدا وارد شوید یا ثبت‌نام کنید.")


@login_required
async def view_transactions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    token = get_token(user_id)
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    async with httpx.AsyncClient(trust_env=True) as client:
        try:
            r = await client.get(f"{settings.backend_url}/transactions", headers=headers, timeout=10)
            if r.status_code == 200:
                transactions = r.json()
                if not transactions:
                    await update.message.reply_text("تراکنشی یافت نشد.")
                    return
                text = "\n".join([f"{t.get('id')}: {t.get('amount')} تومان" for t in transactions])
                await update.message.reply_text(f"تراکنش‌های شما:\n{text}")
            else:
                await update.message.reply_text("خطا در دریافت تراکنش‌ها.")
        except Exception:
            logger.exception("Error while fetching transactions")
            await update.message.reply_text("خطا در ارتباط با سرور. لطفاً بعداً تلاش کنید.")
