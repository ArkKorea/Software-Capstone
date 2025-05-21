#qr 혹은 바코드 처리 진입점
from typing import Union
from app.schemas.product import ProductResponse, ProductRequest, BundleResponse, ProductCreate, ProductCreateResponse, ProductUpdate, ProductDelete
from app.services.product_service import decode_barcode, decode_qrcode, create_product_service, get_my_products_service, update_product_service, delete_product_service
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

# 내 상품 등록
@router.post("/supplier/products/create", response_model=ProductCreateResponse)
def create_product(
    request: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_product_service(db, request, current_user)

# 내 상품 조회
@router.post("/api/supplier/products/list", response_model=list[ProductResponse])
def get_my_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_my_products_service(db, current_user)

# 내 상품 수정
@router.post("/api/supplier/products/update")
def update_product(
    request: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_product_service(db, request, current_user)

# 내 상품 삭제
@router.post("/api/supplier/products/delete")
def delete_product(
    request: ProductDelete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_product_service(db, request, current_user)
