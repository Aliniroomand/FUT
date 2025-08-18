from bot.proxy import get_httpx_client
from bot.config import settings

BASE_URL = settings.backend_url

async def get_health():
    client = await get_httpx_client()
    r = await client.get(f"{BASE_URL}/health")
    r.raise_for_status()
    return r.json()

async def register_user(data: dict):
    client = await get_httpx_client()
    r = await client.post(f"{BASE_URL}/register", json=data)
    r.raise_for_status()
    return r.json()

async def login_user(data: dict):
    client = await get_httpx_client()
    r = await client.post(f"{BASE_URL}/login", json=data)
    r.raise_for_status()
    return r.json()
