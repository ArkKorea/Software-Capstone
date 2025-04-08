from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from app.services.auth_service import login_user, register_user
from app.db.database import get_db  # DB 연결 방식에 따라 수정 필요

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(request, db)

@router.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(request, db)