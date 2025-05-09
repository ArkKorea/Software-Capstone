from app.schemas.allergen import *
from app.core.auth import get_current_user
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.crud.allergen import *

def get_user_allergies(db: Session, current_user: User = Depends(get_current_user)) -> AllergenGetResponse:
    allergies = get_allergies_by_user_id(current_user.id, db)
    if not allergies:
        return AllergenGetResponse(allergies=[])
    return AllergenGetResponse(allergies=[allergy.name for allergy in allergies])

def save_user_allergies(request: AllergenSaveRequest, db: Session, current_user: User = Depends(get_current_user)) -> AllergenSaveResponse:
    save_allergies_by_user_id(current_user, request.allergies, db)
    return AllergenSaveResponse(message="알러지 정보가 저장되었습니다.")