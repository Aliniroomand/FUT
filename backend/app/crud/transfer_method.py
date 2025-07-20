from sqlalchemy.orm import Session
from app.models.transfer_method import TransferMethod
from app.schemas.transfer_method import TransferMethodCreate, TransferMethodUpdate

def get_all(db: Session):
    return db.query(TransferMethod).all()

def get_by_id(db: Session, id: int):
    return db.query(TransferMethod).filter(TransferMethod.id == id).first()

def create(db: Session, method: TransferMethodCreate):
    db_method = TransferMethod(
        name=method.name,
        description=method.description,
        is_active=method.is_active,
    )
    db.add(db_method)
    db.commit()
    db.refresh(db_method)
    return db_method

def update(db: Session, id: int, method: TransferMethodUpdate):
    db_method = get_by_id(db, id)
    if not db_method:
        return None
    for key, value in method.dict(exclude_unset=True).items():
        setattr(db_method, key, value)
    db.commit()
    db.refresh(db_method)
    return db_method

def delete(db: Session, id: int):
    db_method = get_by_id(db, id)
    if not db_method:
        return None
    db.delete(db_method)
    db.commit()
    return True
