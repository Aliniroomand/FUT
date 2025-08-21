import logging
import asyncio

logger = logging.getLogger(__name__)

async def emit_admin(event: str, payload: dict):
    """Stub to push websocket events to admin panel. Replace with real websocket client.
    Runs asynchronously and logs event for now.
    """
    try:
        logger.info("WS EMIT %s %s", event, payload)
        # TODO: implement real websocket push using websockets or aiohttp
    except Exception:
        logger.exception("Failed to emit websocket event")
