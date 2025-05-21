#qr 혹은 바코드 처리 진입점
from typing import Union
from app.schemas.product import ProductResponse, ProductRequest, BundleResponse, ProductCreate, ProductCreateResponse
from app.services.product_service import decode_barcode, decode_qrcode, create_product_service
from app.db.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/from-code", response_model=Union[ProductResponse, BundleResponse])
def code_scanner(request: ProductRequest,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    code_type = request.type
    if code_type == "barcode":
        return decode_barcode(request.value, db, current_user)
    elif code_type == "qrcode":
        return decode_qrcode(request.value, db, current_user)
    else:
        raise HTTPException(status_code=400,
                            detail="유효하지 않은 요청 타입입니다. 'barcode' 또는 'qrcode'를 입력해주세요.")
    
@router.post("/product", response_model=ProductCreateResponse)
def create_product(
    request: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_product_service(db, request, current_user)