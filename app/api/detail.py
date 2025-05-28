from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.product import ProductResponse, BundleResponse
from app.schemas.supplier import SupplierDetailResponse
from app.db.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.detail_service import get_product_detail_service, get_bundle_detail_service, get_supplier_detail_service

router = APIRouter()

# 개별 상품 상세정보
@router.get("/product/{product_id}", response_model=ProductResponse)
def get_product_detail(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_product_detail_service(db, product_id, current_user)

# 번들 상세정보
@router.get("/bundle/{bundle_id}", response_model=BundleResponse)
def get_bundle_detail(
    bundle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_bundle_detail_service(db, bundle_id, current_user)

# 공급자(상점페이지) 상세정보
@router.get("/supplier/{supplier_id}", response_model=SupplierDetailResponse)
def get_supplier_detail(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_supplier_detail_service(db, supplier_id, current_user)
