
import httpx
from bs4 import BeautifulSoup

async def fetch_player_price(player_id: int, slug: str, platform: str) -> dict:
    """
    تلاش برای گرفتن قیمت واقعی بازیکن از سایت futbin.
    خروجی: دیکشنری شامل price یا error
    """
    url = f"https://www.futbin.com/25/player/{player_id}/{slug}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, headers=headers)

        if r.status_code != 200:
            return {"error": f"http_{r.status_code}"}

        soup = BeautifulSoup(r.text, "html.parser")

        # پیدا کردن بخش قیمت
        price_box = soup.find("div", class_="price-box player-price-not-ps price-box-original-player")
        price_text = None

        if price_box:
            for div in price_box.find_all("div", class_=lambda x: x and "price" in x):
                if div.find("img", alt="Coin"):
                    price_text = div.get_text(strip=True)
                    break

        if not price_text:
            return {"error": "price_not_found"}

        return {"price": price_text}

    except Exception as e:
        return {"error": f"exception: {str(e)}"}
