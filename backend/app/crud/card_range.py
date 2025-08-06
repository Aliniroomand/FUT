from sqlalchemy.orm import Session
from app.models.card_range import CardRange
from app.schemas.card_range import CardRangeCreate

def create_card_range(db: Session, range_data: CardRangeCreate):
    db_range = CardRange(
        min_value=range_data.min_value,
        max_value=range_data.max_value,
        description=range_data.description,
        primary_card_id=range_data.primary_card_id,
        fallback_card_id=range_data.fallback_card_id,
        transfer_method_id=range_data.transfer_method_id 
    )
    db.add(db_range)
    db.commit()
    db.refresh(db_range)
    return db_range


def get_ranges_for_amount(db: Session, amount: float):
    return db.query(CardRange).filter(
        CardRange.min_value <= amount,
        CardRange.max_value >= amount
    ).all()