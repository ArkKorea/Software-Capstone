from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.db.database import get_db
from app.models import User
from app.schemas.ocr import OCRProductResponse
from app.services.ocr_service import analyze_product_from_base64

router = APIRouter()

@router.post("/product/from-ocr", response_model=OCRProductResponse)
def from_ocr_base64(
    product_name: str = Body(...),
    image_base64: str = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return analyze_product_from_base64(product_name, image_base64, db, current_user)
