from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import get_current_user
from app.models import User
from app.schemas.ocr import OCRProductResponse
from app.services.ocr_service import analyze_product_from_ocr

router = APIRouter()

@router.post("/product/from-ocr", response_model=OCRProductResponse)
def from_ocr(
    product_name: str = Form(...),
    image_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return analyze_product_from_ocr(product_name, image_file, db, current_user)
