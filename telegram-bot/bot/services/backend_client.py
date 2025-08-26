# /services/backend_clien
import logging
import asyncio
from typing import Any, Dict
from urllib.parse import urlparse

import httpx

from bot.proxy import get_httpx_client
from bot.config import settings

logger = logging.getLogger(__name__)

# Assumption: repository does not define a global REQUEST_TIMEOUT constant.
# Use a reasonable default here. If the project defines a different value
# later, we can import/replace it.
REQUEST_TIMEOUT = 10

BASE_URL = settings.backend_url


def _is_local_url(url: str) -> bool:
    try:
        host = (urlparse(url).hostname or "").lower()
        return host in ("127.0.0.1", "localhost", "::1")
    except Exception:
        return False


async def _request(method: str, url: str, **kwargs) -> httpx.Response:
    """Send request, bypassing proxy for localhost by using a fresh client.

    For non-local URLs reuse the shared client from proxy.get_httpx_client().
    """
    if _is_local_url(url):
        # create a short-lived client that does not use proxies/environment
        # Important: set trust_env=False so system env proxies are ignored
        timeout = kwargs.pop('timeout', REQUEST_TIMEOUT)
        logger.debug("backend_client: sending local request without proxy to %s", url)
        async with httpx.AsyncClient(timeout=timeout, trust_env=False) as client:
            kwargs.setdefault('follow_redirects', True)
            return await client.request(method, url, **kwargs)
    client = await get_httpx_client()
    kwargs.setdefault('follow_redirects', True)
    return await client.request(method, url, **kwargs)


async def create_transaction(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Create a transaction in backend.

    Expected payload shape (suggested):
    {
      "user_id": <int|str>,
      "direction": "sell"|"buy",
      "method_id": <int>,
      "player_id": <int|null>,
      "amount_requested": <int>,
      "transfer_multiplier": <float>,
      "status": "pending",
      "meta": {}
    }

    Raises httpx exceptions for network/timeouts and raises for non-2xx
    responses. Ensures returned transaction contains `id` and `tracking_id`.
    """
    url = f"{BASE_URL}/transactions"
    r = await _request('POST', url, json=payload, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    data = r.json()

    # Ensure minimal contract: created transaction must include id and tracking_id
    if not isinstance(data, dict):
        logger.error("create_transaction: unexpected response type: %s", type(data))
        raise ValueError("unexpected response from backend when creating transaction")

    if "id" not in data or "tracking_id" not in data:
        logger.error("create_transaction: missing id/tracking_id in response: %s", data)
        raise ValueError("backend did not return id and tracking_id for created transaction")

    return data


async def update_transaction(tx_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Patch an existing transaction.

    Examples of payloads:
      - success: {"status":"success","fut_purchase_info":{...}}
      - failed: {"status":"failed","fail_reason":"timeout|user_cancel|not_purchased"}
    Partial updates are allowed.
    """
    url = f"{BASE_URL}/transactions/{tx_id}"
    r = await _request('PATCH', url, json=payload, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()


async def post_alert(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Post an alert to the backend alerts endpoint.

    Expected to return the created alert as a JSON dict.
    """
    url = f"{BASE_URL}/alerts"
    r = await _request('POST', url, json=payload, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()


async def list_transfer_methods() -> list[Dict[str, Any]]:
    """Return list of transfer methods from backend."""
    url = f"{BASE_URL}/transfer-methods"
    r = await _request('GET', url, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()


async def get_transfer_method(method_id: int) -> Dict[str, Any]:
    url = f"{BASE_URL}/transfer-methods/{method_id}"
    r = await _request('GET', url, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()


async def list_card_ranges() -> list[Dict[str, Any]]:
    url = f"{BASE_URL}/card-ranges"
    r = await _request('GET', url, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()


async def get_player_card_meta(player_id: int) -> Dict[str, Any]:
    url = f"{BASE_URL}/player_card/{player_id}"
    r = await _request('GET', url, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()


async def get_transaction_status() -> Dict[str, Any]:
    url = f"{BASE_URL}/transaction-status"
    last_exc: Exception | None = None
    # retry once on 5xx transient errors
    for attempt in range(2):
        try:
            r = await _request('GET', url, timeout=REQUEST_TIMEOUT)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as exc:
            last_exc = exc
            status = exc.response.status_code if exc.response is not None else None
            # retry on server errors (5xx)
            if status is not None and 500 <= status < 600 and attempt == 0:
                await asyncio.sleep(0.2)
                continue
            raise
        except Exception as exc:
            last_exc = exc
            # network or other error - don't retry
            raise
    # if we exit loop, raise last exception
    if last_exc:
        raise last_exc
    # fallback (shouldn't reach)
    raise RuntimeError("failed to fetch transaction status")
