from app.schemas.symptom import *
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from fastapi import Depends
from app.models.user import User
from app.crud.symptom import *

def save_user_symptom(request: SymptomSaveRequest, db: Session, current_user: User = Depends(get_current_user)) -> SymptomSaveResponse:
    return

def get_user_symptom(request: SymptomByDateRequest, db: Session, current_user: User = Depends(get_current_user)) -> SymptomByDateResponse:
    return