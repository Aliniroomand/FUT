import httpx
from bs4 import BeautifulSoup
import asyncio

async def main():
    player_id = 38758
    slug = "takefusa-kubo"
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
            price_div = soup.select("div.price inline-with-icon lowest-price-1")
            print("ine:",price_div)
            if price_div:
                price_text = price_div.get_text(strip=True)
                print("Extracted price:", price_text)
            else:
                print("Price div not found!")

asyncio.run(main())



