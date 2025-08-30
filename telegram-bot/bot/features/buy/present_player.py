import logging
from bot.services.backend_client import list_card_ranges, get_player_card_meta  
from bot.ui.buy_messages import out_of_range_text, build_card_info_text

logger = logging.getLogger(__name__)

async def present_player_for_amount(amount: float):
    ranges = await list_card_ranges()
    selected = None
    for r in ranges:
        min_v = r.get("min_value") or r.get("min")
        max_v = r.get("max_value") or r.get("max")
        try:
            if min_v is None or max_v is None:
                continue
            if float(min_v) <= float(amount) <= float(max_v):
                selected = r
                break
        except Exception:
            continue

    if not selected:
        logger.info("Amount %s is out of ranges", amount)
        return {"type": "admin", "text": out_of_range_text(amount)}

    primary_card_id = selected.get("primary_card_id")
    fallback_card_id = selected.get("fallback_card_id")
    transfer_method = selected.get("transfer_method") or {}
    transfer_multiplier = transfer_method.get("transfer_multiplier") or transfer_method.get("multiplier") or 1.0

    # Fetch primary safely
    try:
        primary_card = await get_player_card_meta(primary_card_id)
    except Exception as e:
        logger.exception("Failed to fetch primary card %s: %s", primary_card_id, e)
        primary_card = None

    if not primary_card:
        return {"type": "admin", "text": "خطا در دریافت اطلاعات کارت — لطفاً بعداً تلاش کنید یا با ادمین تماس بگیرید."}

    fallback_card = None
    if fallback_card_id:
        try:
            fallback_card = await get_player_card_meta(fallback_card_id)
        except Exception:
            fallback_card = None

    text = build_card_info_text(selected, primary_card, fallback_card or {}, float(transfer_multiplier), amount)

    return {
        "type": "player",
        "text": text,
        "range_id": selected.get("id"),
        "primary_card_id": primary_card_id,
        "fallback_card_id": fallback_card_id
    }
