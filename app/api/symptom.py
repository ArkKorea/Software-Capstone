from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.symptom import *
from app.core.auth import get_current_user
from app.db.database import get_db
from app.services.symptom_service import *

router = APIRouter()

@router.post("/save", response_model=SymptomSaveResponse)
def save_symptom(request: SymptomSaveRequest,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    return save_user_symptom(request, db, current_user)

@router.post("/by-date", response_model=SymptomByDateResponse)
def get_symptom_by_date(request: SymptomByDateRequest,
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    return get_user_symptom_by_date(request, db, current_user)