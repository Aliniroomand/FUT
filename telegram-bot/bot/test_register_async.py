import asyncio
import httpx
from bot.config import settings

async def test():
    payload = {"phone_number": "09123456789", "email": "devtest@example.com", "password": "456789"}
    async with httpx.AsyncClient(trust_env=False) as client:
        try:
            r = await client.post(f"{settings.backend_url}/auth/register", json=payload, timeout=10)
            print('status', r.status_code)
            print('headers', r.headers)
            try:
                print('json', r.json())
            except Exception:
                print('text', r.text)
        except Exception as e:
            print('error', e)

asyncio.run(test())
