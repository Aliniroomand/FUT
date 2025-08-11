from sqlalchemy.orm import Session
from app.models.ea_account import EAAccount
from app.schemas.ea_account import EAAccountCreate

def create_ea_account(db: Session, account: EAAccountCreate):
	db_account = EAAccount(
		name=account.name,
		email=account.email,
		platform=account.platform,
		daily_limit=account.daily_limit,
		is_user_account=account.is_user_account
	)
	db.add(db_account)
	db.commit()
	db.refresh(db_account)
	return db_account

def delete_ea_account(db: Session, account_id: int):
	account = db.query(EAAccount).filter(EAAccount.id == account_id).first()
	if account:
		db.delete(account)
		db.commit()
		return True
	return False
