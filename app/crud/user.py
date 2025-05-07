from sqlalchemy.orm import Session
from app.models.models import Users

def get_user_by_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()