from sqlalchemy.orm import Session
from app.models.transfer_method import TransferMethod
from app.schemas.transfer_method import TransferMethodCreate, TransferMethodUpdate
from app.models.card_range import CardRange

def get_all(db: Session):
    return db.query(TransferMethod).all()

def get(db: Session, id: int):
    return db.query(TransferMethod).filter(TransferMethod.id == id).first()

def create(db: Session, method: TransferMethodCreate):
    db_method = TransferMethod(
        name=method.name,
        description=method.description,
        is_active=method.is_active,
        logic=method.logic
    )
    db.add(db_method)
    db.commit()
    db.refresh(db_method)
    return db_method

def update(db: Session, id: int, method: TransferMethodUpdate):
    db_method = get(db, id)
    if not db_method:
        return None
    
    if method.name is not None:
        db_method.name = method.name
    if method.description is not None:
        db_method.description = method.description
    if method.is_active is not None:
        db_method.is_active = method.is_active
    if method.logic is not None:
        db_method.logic = method.logic
    
    db.commit()
    db.refresh(db_method)
    return db_method

def delete(db: Session, id: int):
    db_method = get(db, id)
    if not db_method:
        return False
    db.delete(db_method)
    db.commit()
    return True

def get_ranges_for_method(db: Session, method_id: int):
    return db.query(CardRange).filter(CardRange.transfer_method_id == method_id).all()