from sqlalchemy.orm import Session
from app.models.transactionsControl import TransactionStatus

def get_status(db: Session):
    status = db.query(TransactionStatus).first()
    if not status:
        status = TransactionStatus()
        db.add(status)
        db.commit()
        db.refresh(status)
    return status

def update_status(db: Session, buying_disabled=None, selling_disabled=None):
    status = get_status(db)
    if buying_disabled is not None:
        status.buying_disabled = buying_disabled
    if selling_disabled is not None:
        status.selling_disabled = selling_disabled
    db.commit()
    db.refresh(status)
    return status
