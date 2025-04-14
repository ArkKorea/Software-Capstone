from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import (
    LoginRequest, LoginResponse,
    RegisterRequest, RegisterResponse,
    EmailVerificationResponse,
    ResetPasswordRequest, ResetPasswordConfirm, MessageResponse
)
from app.services.auth_service import (
    login_user, register_user, verify_user,
    request_password_reset, reset_password
)
from app.db.database import get_db

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(request, db)

@router.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(request, db)

@router.get("/verify", response_model=EmailVerificationResponse)
def verify_email(token: str, db: Session = Depends(get_db)):
    return verify_user(token, db)

# 비밀번호 재설정 요청
@router.post("/reset-password-request", response_model=MessageResponse)
def reset_password_request(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    return request_password_reset(request, db)

# 비밀번호 재설정 실행
@router.post("/reset-password", response_model=MessageResponse)
def confirm_reset_password(request: ResetPasswordConfirm, db: Session = Depends(get_db)):
    return reset_password(request, db)