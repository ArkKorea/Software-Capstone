from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.core.auth import get_current_user
from app.schemas.food_bundle import BundleCreate, BundleListResponse, BundleUpdate,  BundleDelete
from app.services.bundle import create_bundle_service, get_my_bundles_service, update_bundle_service, delete_bundle_service
router = APIRouter()

# 번들 생성
@router.post("/create")
def create_bundle(
    request: BundleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_bundle_service(db, request, current_user)

@router.post("/list", response_model=BundleListResponse)
def list_my_bundles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_my_bundles_service(db, current_user)

# 번들 수정
@router.post("/update")
def update_bundle(
    request: BundleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_bundle_service(db, request, current_user)

# 번들 삭제
@router.post("/delete")
def delete_bundle(
    request: BundleDelete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_bundle_service(db, request, current_user)