from sqlalchemy.orm import Session
from app.models.player_card import PlayerCard
from app.schemas.player_card import PlayerCardCreate, PlayerCardUpdate
from typing import Optional




def create_player_card(db: Session, player_card: PlayerCardCreate) -> PlayerCard:
    obj = PlayerCard(
    id=player_card.id, # allow explicit admin-set id; DB will ignore None and autoincrement
    name=player_card.name,
    version=player_card.version,
    rating=player_card.rating,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj




def get_player_cards(db: Session):
    return db.query(PlayerCard).all()




def get_player_card(db: Session, card_id: int) -> Optional[PlayerCard]:
    return db.query(PlayerCard).filter(PlayerCard.id == card_id).first()




def update_player_card(db: Session, card_id: int, updates: PlayerCardUpdate) -> Optional[PlayerCard]:
    obj = get_player_card(db, card_id)
    if not obj:
        return None
    if updates.name is not None:
        obj.name = updates.name
    if updates.version is not None:
        obj.version = updates.version
    if updates.rating is not None:
        obj.rating = updates.rating
    db.commit()
    db.refresh(obj)
    return obj




def delete_player_card(db: Session, card_id: int) -> bool:
    obj = get_player_card(db, card_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True