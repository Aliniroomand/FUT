from sqlalchemy.orm import Session
from app.models.card_range import CardRange
from app.schemas.card_range import CardRangeCreate

def get_all(db: Session):
    return db.query(CardRange).all()

def create(db: Session, card_range: CardRangeCreate):
    db_card_range = CardRange(**card_range.dict())
    db.add(db_card_range)
    db.commit()
    db.refresh(db_card_range)
    return db_card_range

def update(db: Session, id: int, card_range: CardRangeCreate):
    db_card_range = db.query(CardRange).filter(CardRange.id == id).first()
    if not db_card_range:
        return None
    for key, value in card_range.dict().items():
        setattr(db_card_range, key, value)
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
