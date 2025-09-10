import aiohttp
import httpx
import requests
import urllib.parse
from bot.config import settings

# --------------------
# requests (sync)
# --------------------
def get_requests_session(no_proxies: bool = False) -> requests.Session:
    """Return a configured requests.Session.

    If no_proxies is True, the session will not use the configured proxy
    (useful for localhost/backend calls). Otherwise, proxies from settings
    are applied when present.
    """
    session = requests.Session()
    # ensure system env proxies are not accidentally used when no_proxies
    if no_proxies:
        session.trust_env = False
        return session

    if settings.http_proxy or settings.https_proxy:
        proxy_url = settings.https_proxy or settings.http_proxy
        session.proxies.update({
            "http": proxy_url,
            "https": proxy_url,
        })
    return session


def requests_get(url: str, timeout: int = 10, headers: dict | None = None) -> requests.Response | None:
    """Perform a GET request using proxy for remote hosts and bypass proxy for localhost.

    Returns the requests.Response on success or None on exception.
    Accepts optional headers dict.
    """
    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or '').lower()
    # treat localhost addresses as local (bypass proxy)
    no_proxies = host in ('127.0.0.1', 'localhost', '::1')
    sess = get_requests_session(no_proxies=no_proxies)
    try:
        if headers:
            return sess.get(url, timeout=timeout, headers=headers)
        return sess.get(url, timeout=timeout)
    except Exception:
        # caller will handle logging/emits
        return None


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
