from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud.user import get_user_by_email, create_user
from app.core.security import verify_password, create_access_token
from app.schemas.auth import LoginRequest, LoginResponse, UserOut
from app.schemas.auth import RegisterRequest, RegisterResponse
from app.core.security import hash_password
import uuid

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

def register_user(request: RegisterRequest, db: Session) -> RegisterResponse:
    if not request.agree_personal_info:
        raise HTTPException(status_code=400, detail="개인정보 수집 및 이용에 동의해야 합니다.")

    existing_user = get_user_by_email(db, request.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="이미 등록된 이메일입니다.", headers={"X-Error-Code": "EMAIL_ALREADY_EXISTS"})

    if len(request.password) < 8:
        raise HTTPException(status_code=400, detail="비밀번호는 8자 이상이어야 합니다.", headers={"X-Error-Code": "INVALID_PASSWORD_FORMAT"})

    # 비밀번호 해싱
    password_hash = hash_password(request.password)

    # 이메일 인증 토큰 생성
    email_token = str(uuid.uuid4())

    # 유저 생성
    create_user(db, request, password_hash, email_token)

    # 추후 이메일 발송 추가 예정
    return RegisterResponse(message="이메일 인증 링크가 발송되었습니다.")