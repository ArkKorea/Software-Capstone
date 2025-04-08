from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import RegisterRequest
from datetime import datetime

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# 유저 생성 함수
def create_user(db: Session, user_data: RegisterRequest, password_hash: str, email_token: str) -> User:
    new_user = User(
        email=user_data.email,
        password_hash=password_hash,
        birth=user_data.birthdate,
        role="consumer",  # 기본값으로 consumer 지정
        is_verified=False,
        email_verification_token=email_token,
        terms_version_id=1,  # 현재 active terms_version_id가 1이라는 가정
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user