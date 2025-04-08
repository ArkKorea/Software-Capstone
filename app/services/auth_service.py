from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud.user import get_user_by_email
from app.core.security import verify_password, create_access_token
from app.schemas.auth import LoginRequest, LoginResponse, UserOut

from app.core.config import settings  # SECRET_KEY 가져오기

def login_user(request: LoginRequest, db: Session):
    user = get_user_by_email(db, request.email)
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 일치하지 않습니다.")
    
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="이메일 인증이 완료되지 않았습니다.", headers={"X-Error-Code": "EMAIL_NOT_VERIFIED"})
    
    access_token = create_access_token(
    {"user_id": user.id},
    secret_key=settings.SECRET_KEY  # SECRET_KEY 테스트 용도
    )

    return LoginResponse(
        access_token=access_token,
        user=UserOut(
            user_id=str(user.id),
            email=user.email,
        )
    )