from sqlalchemy.orm import Session
from app.models.card_range_assignment import CardRangeAssignment
from app.schemas.card_range_assignment import CardRangeAssignmentCreate 

def create_range_assignment(db: Session, data: CardRangeAssignmentCreate):
    db_range = CardRangeAssignment(**data.model_dump())
    db.add(db_range)
    db.commit()
    db.refresh(db_range)
    return db_range

def get_ranges_by_method(db: Session, method_id: int):
    return db.query(CardRangeAssignment).filter(CardRangeAssignment.method_id == method_id).all()
