from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import RegisterRequest
from datetime import datetime, timedelta

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

# 이메일 인증증
# 이메일 인증 토큰으로 유저 찾기
def get_user_by_verification_token(db: Session, token: str) -> User | None:
    print(">>> 쿼리용 토큰:", repr(token))  # 공백 유무 확인
    user = db.query(User).filter(User.email_verification_token == token).first()
    print(">>> 결과:", user)
    return user

# 이메일 인증 완료 처리
def verify_user_email(db: Session, user: User):
    user.is_verified = True
    user.email_verification_token = None  # 재사용 방지
    db.commit()
    db.refresh(user)

# 비밀번호 재설정
# 비밀번호 재설정 토큰 저장
def set_reset_token(db: Session, user: User, token: str, expires_minutes: int = 30):
    user.reset_password_token = token
    user.reset_password_expires_at = datetime.utcnow() + timedelta(minutes=expires_minutes)
    db.commit()
    db.refresh(user)

# 비밀번호 재설정 인증 토큰으로 유저 찾기
def get_user_by_reset_token(db: Session, token: str) -> User | None:
    return db.query(User).filter(User.reset_password_token == token).first()

# 비밀번호 변경 및 토큰 무효화
def update_user_password(db: Session, user: User, new_password_hash: str):
    user.password_hash = new_password_hash
    user.reset_password_token = None
    user.reset_password_expires_at = None
    db.commit()
    db.refresh(user)