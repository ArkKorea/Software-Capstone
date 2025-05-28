from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.allergen import AllergenGetResponse, AllergenSaveRequest, AllergenSaveResponse
from app.services.allergen_service import get_user_allergies, save_user_allergies
router = APIRouter()

@router.post("/get", response_model=AllergenGetResponse)
def get_allergies(db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    return get_user_allergies(db, current_user)


@router.post("/save", response_model=AllergenSaveResponse)
def save_allergies(request: AllergenSaveRequest,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    return save_user_allergies(request, db, current_user)