# app/api/favorite.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.favorite_service import (
    toggle_favorite,
    get_favorites
)
from app.schemas.favorite import (
    FavoriteActionRequest,
    FavoriteListResponse,
    FavoriteType
)

from app.models.user import User
from app.core.auth import get_current_user  # 인증 유저 가져오기기

router = APIRouter()

# 즐겨찾기 등록/삭제
@router.post("/favorites")
def favorite_action(
    request: FavoriteActionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = toggle_favorite(request, current_user.id, db)
    return {"message": message}

# 즐겨찾기 조회(매장)
@router.get("/favorites/suppliers", response_model=FavoriteListResponse)
def get_supplier_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_favorites(current_user.id, FavoriteType.supplier, db)

# 즐겨찾기 조회(food + bundle)
@router.get("/favorites/products", response_model=FavoriteListResponse)
def get_product_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_favorites(current_user.id, FavoriteType.food, db)
