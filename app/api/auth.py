from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import login_user
from app.db.database import get_db  # DB 연결 방식에 따라 수정 필요

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(request, db)
