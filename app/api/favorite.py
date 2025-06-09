from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.favorite_service import toggle_favorite, get_favorites
from app.schemas.favorite import (
    FavoriteActionRequest,
    FavoriteListResponse,
)

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

# 즐겨찾기 조회(단품)
@router.get("/favorites/foods", response_model=FavoriteListResponse)
def get_food_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_favorites(user_id=current_user.id, db=db, target="food")

# 즐겨찾기 조회(번들)
@router.get("/favorites/bundles", response_model=FavoriteListResponse)
def get_bundle_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_favorites(user_id=current_user.id, db=db, target="bundle")

# 즐겨찾기 조회(공급자)
@router.get("/favorites/suppliers", response_model=FavoriteListResponse)
def get_supplier_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_favorites(user_id=current_user.id, db=db, target="supplier")
