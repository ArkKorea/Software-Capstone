from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from email.mime.text import MIMEText
import uuid
import smtplib

# 보안
from app.core.security import (
    verify_password, 
    create_access_token, 
    hash_password
)

# 설정
from app.core.config import settings  # SECRET_KEY 가져오기

# CRUD
from app.crud.user import (
    get_user_by_email,
    create_user,
    get_user_by_verification_token,
    verify_user_email,
    set_reset_token,
    get_user_by_reset_token,
    update_user_password
)

# 스키마
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    UserOut,
    RegisterRequest,
    RegisterResponse,
    EmailVerificationResponse,
    ResetPasswordRequest,
    ResetPasswordConfirm,
    MessageResponse
)


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
    send_verification_email(request.email, email_token)
    return RegisterResponse(message="이메일 인증 링크가 발송되었습니다.")


# 인증용 이메일 발송
def send_verification_email(to_email: str, token: str):
    verify_url = f"http://localhost:8000/api/auth/verify?token={token}"
    subject = "이메일 인증을 완료해 주세요"
    body = f"""
    아래 링크를 클릭하여 이메일 인증을 완료해 주세요:

    {verify_url}

    이 링크는 일정 시간 후 만료될 수 있습니다.
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "allertsign@gmail.com"
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("allertsign@gmail.com", "lwiz gvnf tqlc tcgr")
        server.send_message(msg)


def verify_user(token: str, db: Session) -> EmailVerificationResponse:
    user = get_user_by_verification_token(db, token)
    
    if not user:
        raise HTTPException(status_code=400, detail="토큰이 유효하지 않거나 만료되었습니다.", headers={"X-Error-Code": "INVALID_OR_EXPIRED_TOKEN"})
    
    if user.is_verified:
        raise HTTPException(status_code=409, detail="이메일이 이미 인증되었습니다.", headers={"X-Error-Code": "ALREADY_VERIFIED"})
    
    verify_user_email(db, user)

    return EmailVerificationResponse(message="이메일 인증이 완료되었습니다.")

# 재설정 요청 처리
def request_password_reset(request: ResetPasswordRequest, db: Session) -> MessageResponse:
    user = get_user_by_email(db, request.email)
    if not user or not user.is_verified:
        # 인증된 계정만 비밀번호 재설정 가능
        raise HTTPException(status_code=404, detail="해당 이메일로 가입된 계정을 찾을 수 없습니다.")

    token = str(uuid.uuid4())
    set_reset_token(db, user, token)

    # 실제 배포 전까진 이메일 대신 콘솔에 링크 출력
    print(f"비밀번호 재설정 링크: http://localhost:8000/api/auth/reset-password?token={token}")

    return MessageResponse(message="비밀번호 재설정 링크가 발송되었습니다.")

# 비밀번호 재설정
def reset_password(request: ResetPasswordConfirm, db: Session) -> MessageResponse:
    user = get_user_by_reset_token(db, request.token)
    if not user:
        raise HTTPException(status_code=400, detail="토큰이 유효하지 않거나 만료되었습니다.")

    # 만료 시간 검증
    if user.reset_password_expires_at and user.reset_password_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="토큰이 만료되었습니다.")

    if len(request.new_password) < 8:
        raise HTTPException(status_code=400, detail="비밀번호는 8자 이상이어야 합니다.")

    hashed_pw = hash_password(request.new_password)
    update_user_password(db, user, hashed_pw)

    return MessageResponse(message="비밀번호가 성공적으로 변경되었습니다.")
