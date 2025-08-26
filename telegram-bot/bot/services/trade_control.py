# bot/services/trade_control.py
import asyncio
import inspect
import json
import logging
from typing import Any, Dict, List, Optional

from bot.proxy import requests_get
from bot.config import settings
from bot.services import config_cache, backend_client
from bot.services.ws_client import emit_admin

logger = logging.getLogger(__name__)

def sync_get(url: str, timeout: int = 5):
    try:
        return requests_get(url, timeout=timeout)
    except Exception as exc:
        logger.exception("sync_get failed for url=%s: %s", url, exc)
        try:
            asyncio.get_event_loop().create_task(
                emit_admin('backend:error', {'url': url, 'error': str(exc)[:2000]})
            )
        except Exception:
            logger.exception('failed to schedule emit_admin')
        return None

async def get_status() -> Dict[str, bool]:
    """
    { 'buying_disabled': bool, 'selling_disabled': bool }
    """
    r = sync_get(f"{settings.backend_url}/transaction-status", timeout=5)
    buying_disabled = False
    selling_disabled = False

    if r and getattr(r, 'status_code', None) == 200:
        try:
            ts = r.json()
            buying_disabled = bool(ts.get('buying_disabled', False))
            selling_disabled = bool(ts.get('selling_disabled', False))
        except Exception:
            logger.exception("failed parsing transaction-status json")
    else:
        if r is not None:
            try:
                body = r.text
            except Exception:
                body = '<unreadable>'
            logger.warning('transaction-status returned %s url=%s',
                           getattr(r, 'status_code', None), getattr(r, 'url', None))
            try:
                asyncio.get_event_loop().create_task(emit_admin(
                    'backend:response',
                    {'url': getattr(r, 'url', ''), 'response_text': (body or '')[:2000]}
                ))
            except Exception:
                logger.exception('failed to schedule emit_admin')

    return {'buying_disabled': buying_disabled, 'selling_disabled': selling_disabled}

async def fetch_transfer_methods_with_fallback() -> List[dict]:
    try:
        methods = config_cache.get_transfer_methods(lambda: backend_client.list_transfer_methods())
        if inspect.isawaitable(methods):
            methods = await methods
    except Exception as exc:
        logger.exception("config_cache.get_transfer_methods raised: %s", exc)
        try:
            asyncio.get_event_loop().create_task(emit_admin(
                'backend:error',
                {'source': 'config_cache.get_transfer_methods', 'error': str(exc)[:2000]}
            ))
        except Exception:
            logger.exception('failed to schedule emit_admin')
        methods = []

    if not isinstance(methods, (list, tuple)):
        methods = []

    if not methods:
        logger.info("transfer methods empty — trying backend_client.list_transfer_methods() directly")
        try:
            direct = backend_client.list_transfer_methods()
            if inspect.isawaitable(direct):
                direct = await direct
            if hasattr(direct, 'json') and callable(direct.json):
                try:
                    direct_json = direct.json()
                except Exception:
                    try:
                        direct_json = json.loads(getattr(direct, 'text', '') or '{}')
                    except Exception:
                        direct_json = None
                direct = direct_json
        except Exception as exc:
            logger.exception("backend_client.list_transfer_methods failed: %s", exc)
            try:
                asyncio.get_event_loop().create_task(emit_admin(
                    'backend:error',
                    {'source': 'backend_client.list_transfer_methods', 'error': str(exc)[:2000]}
                ))
            except Exception:
                logger.exception('failed to schedule emit_admin')
            direct = []

        if isinstance(direct, (list, tuple)):
            methods = direct
        elif isinstance(direct, dict) and 'methods' in direct and isinstance(direct['methods'], list):
            methods = direct['methods']
        else:
            try:
                asyncio.get_event_loop().create_task(emit_admin(
                    'backend:unexpected_transfer_methods', {'raw': str(direct)[:4000]}
                ))
            except Exception:
                logger.exception('failed to schedule emit_admin')
            methods = []

    if not isinstance(methods, (list, tuple)):
        methods = []

    return list(methods)

async def fetch_card_ranges() -> List[dict]:
    try:
        ranges = config_cache.get_card_ranges(lambda: backend_client.list_card_ranges())
        if inspect.isawaitable(ranges):
            ranges = await ranges
    except Exception as exc:
        logger.exception("failed to load card ranges: %s", exc)
        try:
            asyncio.get_event_loop().create_task(emit_admin(
                'backend:error', {'source': 'card_ranges', 'error': str(exc)[:2000]}
            ))
        except Exception:
            logger.exception('failed to schedule emit_admin')
        ranges = []

    if not isinstance(ranges, (list, tuple)):
        ranges = []

    return list(ranges)

async def fetch_player_meta(player_id: int) -> dict:
    try:
        meta = config_cache.get_player_card_meta(lambda: backend_client.get_player_card_meta(player_id), player_id)
        if inspect.isawaitable(meta):
            meta = await meta
        if not isinstance(meta, dict):
            return {}
        return meta
    except Exception as exc:
        logger.exception("failed to load player_card %s: %s", player_id, exc)
        try:
            asyncio.get_event_loop().create_task(emit_admin(
                'backend:error', {'source': 'player_card', 'player_id': player_id, 'error': str(exc)[:2000]}
            ))
        except Exception:
            logger.exception('failed to schedule emit_admin')
        return {}


