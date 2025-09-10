from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional ,  List
from pydantic import BaseModel

from app.database import get_db
from app.crud import player_card as crud
from app.crud import price_cache as price_crud
from app.crud import transfer_method as transfer_crud
from app.schemas import player_card as schemas
from app.schemas.price_cache import PriceCacheOut
from app.services.futbin_client import get_player_price
from app.utils.slugify import slugify
from app.utils.rate_limiter import rate_limiter
from app import models

router = APIRouter(prefix="/player-cards", tags=["Player-Cards"])

@router.post("/", response_model=schemas.PlayerCard)
def create_player_card(card: schemas.PlayerCardCreate, db: Session = Depends(get_db)):
    return crud.create_player_card(db, card)

@router.get("/", response_model=list[schemas.PlayerCard])
def list_player_cards(db: Session = Depends(get_db)):
    return crud.get_player_cards(db)

@router.get("/{card_id}", response_model=schemas.PlayerCard)
def get_player_card(card_id: int, db: Session = Depends(get_db)):
    obj = crud.get_player_card(db, card_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Card not found")
    return obj

@router.put("/{card_id}", response_model=schemas.PlayerCard)
def update_player_card(card_id: int, payload: schemas.PlayerCardUpdate, db: Session = Depends(get_db)):
    obj = crud.update_player_card(db, card_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Card not found")
    return obj


# --- NEW: Fetch Futbin price and cache it ---
rl_fetch_price = rate_limiter(limit=5, window_seconds=1, namespace="player.fetch-price")

@router.post("/{card_id}/fetch-price", response_model=PriceCacheOut)
async def fetch_price(card_id: int, platform: str = Query("pc"), db: Session = Depends(get_db)):
    card = crud.get_player_card(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    slug = slugify(card.name)
    res = await get_player_price(str(card.id), platform)
    price = res.get("price")
    if not price:
        raise HTTPException(status_code=502, detail="Futbin price not available")

    cached = price_crud.save(
        db,
        player_id=str(card.id),
        platform=platform,
        price=price,
    )
    return cached

# --- NEW: Compute trade range based on latest cached price and transfer method multiplier ---
class TradeRangeOut(BaseModel):
    min_buy_now: int
    max_buy_now: int
    min_bid: int
    max_bid: int
    base_price: int
    multiplier: float


@router.get("/{card_id}/trade-range", response_model=TradeRangeOut)
def trade_range(card_id: int, method_id: int = Query(...), platform: str = Query("pc"), db: Session = Depends(get_db)):
    card = crud.get_player_card(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    method = transfer_crud.get(db, method_id)
    if not method or not method.transfer_multiplier:
        raise HTTPException(status_code=400, detail="Invalid transfer method")

    latest = price_crud.latest_for(db, player_id=str(card.id), platform=platform)
    if not latest:
        raise HTTPException(status_code=400, detail="No cached price. Call /fetch-price first.")

    base = latest.price
    m = float(method.transfer_multiplier)
    target = int(base * m)

    # Simple, adjustable band around target
    min_buy_now = max(150, int(target * 0.98))
    max_buy_now = int(target * 1.02)
    min_bid = max(150, int(target * 0.95))
    max_bid = int(target * 0.99)

    return TradeRangeOut(
        min_buy_now=min_buy_now,
        max_buy_now=max_buy_now,
        min_bid=min_bid,
        max_bid=max_bid,
        base_price=base,
        multiplier=m,
    )
    
# delete ranges with deleting cards
# ---------------------------------------------------------
# 1) GET dependencies endpoint
# ---------------------------------------------------------
@router.get("/dependencies/{card_id}")
def get_card_dependencies_v2(card_id: int, db: Session = Depends(get_db)):
    """
    Clear endpoint: GET /player-cards/dependencies/{card_id}
    Returns:
      { primary_ranges: [...], fallback_ranges: [...] }
    """
    primary = db.query(models.CardRange).filter(models.CardRange.primary_card_id == card_id).all()
    fallback = db.query(models.CardRange).filter(models.CardRange.fallback_card_id == card_id).all()

    def serialize_range(r):
        return {
            "id": r.id,
            "min_value": r.min_value,
            "max_value": r.max_value,
            "primary_card_id": r.primary_card_id,
            "fallback_card_id": r.fallback_card_id,
            "transfer_method_id": getattr(r, "transfer_method_id", None)
        }

    return {
        "primary_ranges": [serialize_range(r) for r in primary],
        "fallback_ranges": [serialize_range(r) for r in fallback],
    }
# ---------------------------------------------------------
# 2) DELETE with replacement or force cascade
# ---------------------------------------------------------

import logging
logger = logging.getLogger(__name__)

@router.delete("/{card_id}")
def delete_player_card_with_options(
    card_id: int,
    replacement_id: Optional[int] = Query(None, description="If set, replace primary references with this id"),
    force: Optional[bool] = Query(False, description="If true and no replacement_id, delete related ranges"),
    db: Session = Depends(get_db),
):
    """
    Delete a player card with optional replacement or forced cascade.
    - If replacement_id provided: update CardRange.primary_card_id -> replacement_id for ranges referencing card_id.
    - Else if force==True: delete related CardRange rows where primary_card_id == card_id OR fallback_card_id == card_id.
    - Else: if there are related ranges, return 400 with details (caller should ask user for confirmation).
    """
# fetch card
    try:
            card = db.query(models.PlayerCard).filter(models.PlayerCard.id == card_id).first()
            if not card:
                raise HTTPException(status_code=404, detail="PlayerCard not found")

            primary_ranges = db.query(models.CardRange).filter(models.CardRange.primary_card_id == card_id).all()
            fallback_ranges = db.query(models.CardRange).filter(models.CardRange.fallback_card_id == card_id).all()

            if replacement_id is not None:
                if replacement_id == card_id:
                    raise HTTPException(status_code=400, detail="replacement_id cannot be same as deleted card")
                replacement = db.query(models.PlayerCard).filter(models.PlayerCard.id == replacement_id).first()
                if not replacement:
                    raise HTTPException(status_code=400, detail="replacement_id not found")

                # update primary refs → replacement
                for r in primary_ranges:
                    r.primary_card_id = replacement_id
                    db.add(r)

                # update fallback refs هم بهتره همینجا صفر کنیم
                for r in fallback_ranges:
                    r.fallback_card_id = None
                    db.add(r)

                db.delete(card)
                db.commit()
                return {"status": "deleted", "replacement_id": replacement_id, "updated_ranges": [r.id for r in primary_ranges]}

            if (primary_ranges or fallback_ranges) and not force:
                def short(r):
                    return {"id": r.id, "min_value": r.min_value, "max_value": r.max_value}
                raise HTTPException(status_code=409, detail={
                    "message": "card_has_dependencies",
                    "primary_ranges": [short(r) for r in primary_ranges],
                    "fallback_ranges": [short(r) for r in fallback_ranges],
                })

            for r in primary_ranges + fallback_ranges:
                db.delete(r)
            db.delete(card)
            db.commit()
            return {"status": "deleted", "deleted_ranges": [r.id for r in (primary_ranges + fallback_ranges)]}

    except Exception as e:
        logger.exception("Delete player card failed")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"delete_failed: {str(e)}")