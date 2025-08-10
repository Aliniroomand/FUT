from sqlalchemy.orm import Session
from app.models.user import User, UserProfile

def get_full_profile_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None, None
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    return user, profile
