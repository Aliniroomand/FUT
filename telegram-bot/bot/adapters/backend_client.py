# BOT/bot/adapters/backend_client.py
import asyncio
import httpx
from bot.config import settings
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

BASE_URL = getattr(settings, "backend_url", "http://localhost:8000")
TIMEOUT = httpx.Timeout(10.0, connect=5.0)

# ----------------------
# تابع کمکی retry
# ----------------------
async def request_with_retry(method: str, url: str, json: dict | None = None, max_retries: int = 3):
    backoff = 0.5
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                resp = await client.request(method, url, json=json)
                resp.raise_for_status()
                return resp.json()
        except (httpx.HTTPError, httpx.ReadTimeout) as e:
            logger.warning("Attempt %s failed for %s: %s", attempt + 1, url, e)
            if attempt == max_retries - 1:
                logger.error("All retries failed for %s", url)
                raise
            await asyncio.sleep(backoff * (2 ** attempt))

# ----------------------
# تعریف مدل Pydantic برای price
# ----------------------
class PriceResponse(BaseModel):
    price: int | None
    cached: bool
    fetched_at: str
    note: str | None

# ----------------------
# تابعی که پاسخ backend را اعتبارسنجی می‌کند
# ----------------------
async def get_price(item_id: int) -> PriceResponse:
    url = f"{BASE_URL}/price/{item_id}"
    resp_json = await request_with_retry("GET", url)
    try:
        return PriceResponse.parse_obj(resp_json)
    except Exception as e:
        logger.error("Invalid response from backend for item %s: %s", item_id, e)
        # برگردوندن پیام خطای دوستانه بدون crash
        return PriceResponse(price=None, cached=False, fetched_at="", note="خطا در دریافت قیمت")
