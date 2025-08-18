import aiohttp
import httpx
import requests
from bot.config import settings

# --------------------
# requests (sync)
# --------------------
def get_requests_session() -> requests.Session:
    session = requests.Session()
    if settings.http_proxy or settings.https_proxy:
        proxy_url = settings.https_proxy or settings.http_proxy
        session.proxies.update({
            "http": proxy_url,
            "https": proxy_url,
        })
    return session

# --------------------
# aiohttp (async)
# --------------------
_session: aiohttp.ClientSession | None = None
async def get_proxy_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False),
            trust_env=True
        )
    return _session

# --------------------
# httpx (async)
# --------------------
_httpx_client: httpx.AsyncClient | None = None
async def get_httpx_client() -> httpx.AsyncClient:
    global _httpx_client
    if _httpx_client is None:
        proxy_url = settings.https_proxy or settings.http_proxy
        if proxy_url:
            _httpx_client = httpx.AsyncClient(proxies=proxy_url, timeout=10)
        else:
            _httpx_client = httpx.AsyncClient(timeout=10)
    return _httpx_client
