from sqlalchemy.orm import Session
from app.models.price_cache import PriceCache
from typing import Optional




def save(db: Session, *, player_id: str, platform: str, price: int, currency: str = "coins") -> PriceCache:
    row = PriceCache(player_id=str(player_id), platform=platform,  price=int(price), currency=currency)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row




def latest_for(db: Session, *, player_id: str, platform: str) -> Optional[PriceCache]:
    return (
    db.query(PriceCache)
    .filter(PriceCache.player_id == str(player_id), PriceCache.platform == platform)
    .order_by(PriceCache.fetched_at.desc())
    .first()
)