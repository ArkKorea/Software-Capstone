from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.services.meal_service import *
from app.schemas.meal import *
from app.db.database import get_db

router = APIRouter()
#/create 식사기록 저장
@router.post("/create", response_model=CreateMealResponse)
def create_meal(request: CreateMealRequest,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    return create_intake_log(request, db, current_user)

#/select-product 연동 상품 선택
@router.post("/select-product", response_model=ConnectMealResponse)
def connect_meal(request: ConnectMealRequest,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    return connect_intake_log(request, db, current_user)

#/by-date 하루 식사기록 조회
@router.post("/by-date", response_model=QueryMealResponse)
def query_meal(request: QueryMealRequest,
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    return query_intake_log(request, db, current_user)