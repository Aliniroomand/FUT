import httpx
from bs4 import BeautifulSoup
import asyncio

async def main():
    player_id = 45466
    slug = "harry-maguire"
    url = f"https://www.futbin.com/25/player/{player_id}/{slug}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        print("Status:", r.status_code)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")

            # انتخاب دقیق div با سه کلاس
            price_box = soup.find("div", class_="price-box player-price-not-ps price-box-original-player")
            price_text = None

            if price_box:
                # پیدا کردن اولین div که کلاسش با price شروع میشه
                for div in price_box.find_all("div", class_=lambda x: x and "price" in x):
                    if div.find("img", alt="Coin"):  # مطمئن بشیم همون قیمت سکه است
                        price_text = div.get_text(strip=True)
                        break

            if price_text:
                print("Extracted price:", price_text)
            else:
                print("Price not found!")

asyncio.run(main())



