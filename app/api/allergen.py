from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.allergen import AllergenGetResponse, AllergenSaveRequest, AllergenSaveResponse
router = APIRouter()

@router.post("/get")
def get_allergies(request, db: Session = Depends(get_db)):
    return


@router.post("/save", response_model=AllergenSaveResponse)
def save_allergies(request: AllergenSaveRequest, db: Session = Depends(get_db)):
    return AllergenSaveResponse()