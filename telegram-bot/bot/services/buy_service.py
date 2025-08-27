# Developer note:
# Uses backend endpoints:
# - GET /transfer-methods
# - GET /card-ranges
# - GET /player-card/{player_id}
# - POST /transaction (create)
# - PATCH /transaction/{id} (update)
# - GET /user-profile/{user_id}
# - PATCH /user-profile/{user_id}

import functools
import time

_futbin_cache = {}

def _cache_futbin(key, value, ttl=300):
    _futbin_cache[key] = (value, time.time() + ttl)

def _get_futbin_cache(key):
    v = _futbin_cache.get(key)
    if v and v[1] > time.time():
        return v[0]
    return None
async def create_pending_transaction(payload):
    # Thin wrapper for backend call to create transaction
    from bot.services.backend_client import create_transaction
    return await create_transaction(payload)
async def get_player_card_info(player_id):
    # Fetch player info from backend
    from bot.services.backend_client import get_player_card
    player = await get_player_card(player_id)
    # Futbin price (cached)
    price_key = f"price:{player_id}"
    buy_now_price = _get_futbin_cache(price_key)
    if buy_now_price is None:
        from bot.services.futbin import get_price_for_player
        try:
            buy_now_price = await get_price_for_player(player_id)
            _cache_futbin(price_key, buy_now_price)
        except Exception as e:
            buy_now_price = None
            import logging
            logging.error(f"Futbin price error: {e}")
            from bot.services.trade_control import emit_admin
            await emit_admin('futbin:error', {'player_id': player_id, 'error': str(e)})
    # Futbin image (cached)
    image_key = f"image:{player_id}"
    image_url = _get_futbin_cache(image_key)
    if image_url is None:
        from bot.services.futbin import get_image_for_player
        try:
            image_url = await get_image_for_player(player_id)
            _cache_futbin(image_key, image_url)
        except Exception as e:
            image_url = None
            import logging
            logging.error(f"Futbin image error: {e}")
            from bot.services.trade_control import emit_admin
            await emit_admin('futbin:error', {'player_id': player_id, 'error': str(e)})
    return {
        'player': player,
        'buy_now_price': buy_now_price,
        'image_url': image_url
    }
async def get_card_ranges():
    # Thin wrapper for backend call to fetch card ranges
    from bot.services.backend_client import list_card_ranges as backend_get_card_ranges
    return await backend_get_card_ranges()
from bot.services.backend_client import list_transfer_methods as backend_get_transfer_methods


async def get_transfer_methods():
    # Thin wrapper for backend call; expects list of dicts
    # Should call backend_get_transfer_methods (no argument)
    return await backend_get_transfer_methods()

async def get_method(method_id):
    # Thin wrapper for backend call to fetch method by id
    from bot.services.backend_client import get_transfer_method
    return await get_transfer_method(method_id)
