from sqlalchemy.orm import Session
from app.models.card_range import CardRange
from app.schemas.card_range import CardRangeCreate, CardRangeUpdate

def get_all(db: Session):
    return db.query(CardRange).all()

def get(db: Session, id: int):
    return db.query(CardRange).filter(CardRange.id == id).first()

def create(db: Session, card_range: CardRangeCreate):
    db_card_range = CardRange(
        min_value=card_range.min_value,
        max_value=card_range.max_value,
        description=card_range.description,
        transfer_method_id=card_range.transfer_method_id,
        primary_card_id=card_range.primary_card_id,
        fallback_card_id=card_range.fallback_card_id
    )
    db.add(db_card_range)
    db.commit()
    db.refresh(db_card_range)
    return db_card_range

def update(db: Session, id: int, card_range: CardRangeUpdate):
    db_card_range = db.query(CardRange).filter(CardRange.id == id).first()
    if not db_card_range:
        return None
    
    if card_range.min_value is not None:
        db_card_range.min_value = card_range.min_value
    if card_range.max_value is not None:
        db_card_range.max_value = card_range.max_value
    if card_range.description is not None:
        db_card_range.description = card_range.description
    if card_range.transfer_method_id is not None:
        db_card_range.transfer_method_id = card_range.transfer_method_id
    if card_range.primary_card_id is not None:
        db_card_range.primary_card_id = card_range.primary_card_id
    if card_range.fallback_card_id is not None:
        db_card_range.fallback_card_id = card_range.fallback_card_id
    
    db.commit()
    db.refresh(db_card_range)
    return db_card_range

def delete(db: Session, id: int):
    db_card_range = db.query(CardRange).filter(CardRange.id == id).first()
    if not db_card_range:
        return False
    db.delete(db_card_range)
    db.commit()
    return True

def get_ranges_by_card(db: Session, card_id: int):
    return db.query(CardRange).filter(
        (CardRange.primary_card_id == card_id) | 
        (CardRange.fallback_card_id == card_id)
    ).all()