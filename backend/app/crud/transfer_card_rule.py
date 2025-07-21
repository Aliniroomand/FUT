from sqlalchemy.orm import Session
from app.models.transfer_card_rule import TransferCardRule
from app.schemas.transfer_card_rule import TransferCardRuleCreate

def create(db: Session, rule: TransferCardRuleCreate):
    db_rule = TransferCardRule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

def get_all(db: Session):
    return db.query(TransferCardRule).all()

def update(db: Session, rule_id: int, data: TransferCardRuleCreate):
    rule = db.query(TransferCardRule).get(rule_id)
    if not rule:
        return None
    for key, value in data.model_dump().items():
        setattr(rule, key, value)
    db.commit()
    db.refresh(rule)
    return rule

def delete(db: Session, rule_id: int):
    rule = db.query(TransferCardRule).get(rule_id)
    if not rule:
        return False
    db.delete(rule)
    db.commit()
    return True
