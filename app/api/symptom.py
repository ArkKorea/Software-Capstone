from fastapi import APIRouter, Depends
from app.schemas.symptom import *
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.symptom_service import *

router = APIRouter()

#/save 하루 증상 설문 저장
@router.post("/save", response_model=SymptomSaveResponse)
def save_symptom(request: SymptomSaveRequest, db: Session = Depends(get_db)):
    return save_user_symptom(request, db)
#/by-date 하루 증상 설문 조회

@router.post("/by-date", response_model=SymptomByDateResponse)
def get_symptom_by_date(request: SymptomByDateRequest, db: Session = Depends(get_db)):
    return get_user_symptom_by_date(request, db)