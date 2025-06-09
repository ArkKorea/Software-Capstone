from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.favorite_service import toggle_favorite, get_favorite_items, get_favorite_suppliers_with_products
from app.schemas.favorite import (
    FavoriteActionRequest,
)
from app.schemas.search import SearchProductResponse, StoreWithProductsResponse
from app.models.user import User
from app.core.auth import get_current_user  # 인증 유저 가져오기

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


@router.get("/favorites/items", response_model=SearchProductResponse)
def get_my_favorite_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_favorite_items(db, current_user)


@router.get("/favorites/suppliers", response_model=StoreWithProductsResponse)
def get_my_favorite_suppliers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_favorite_suppliers_with_products(db, current_user)
