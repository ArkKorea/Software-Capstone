from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.favorite import FavoriteType
from app.crud.favorite import (
    add_favorite,
    remove_favorite,
    get_favorites_by_type,
    get_favorite_by_type_and_target

)
from app.schemas.favorite import FavoriteListResponse
from app.crud.favorite import get_favorites_by_type, get_food_by_id, get_bundle_by_id, get_supplier_by_id
from app.schemas.favorite import FavoriteActionRequest, FavoriteListResponse, FavoriteOut

# 즐겨찾기 추가/삭제
def toggle_favorite(request: FavoriteActionRequest, user_id: int, db: Session) -> str:
    if request.action == "add":
        # 중복 즐겨찾기 체크
        existing = get_favorite_by_type_and_target(db, user_id, request.type, request.target_id)
        if existing:
            raise HTTPException(status_code=400, detail="이미 즐겨찾기에 등록된 항목입니다.")

        add_favorite(db, user_id, request.type, request.target_id)
        return "즐겨찾기가 추가되었습니다."

    elif request.action == "remove":
        removed = remove_favorite(db, user_id, request.type, request.target_id)
        if not removed:
            raise HTTPException(status_code=404, detail="해당 즐겨찾기를 찾을 수 없습니다.")
        return "즐겨찾기가 삭제되었습니다."

    else:
        raise HTTPException(status_code=400, detail="유효하지 않은 요청입니다.")

# 즐겨찾기 목록 조회
def get_favorites(user_id: int, target_type: FavoriteType, db: Session) -> FavoriteListResponse:
    favorites = get_favorites_by_type(db, user_id, target_type)

    items = []
    for fav in favorites:
        if target_type == FavoriteType.food:
            food = get_food_by_id(db, fav.target_id)
            if food:
                items.append(FavoriteOut.model_validate(food))
        elif target_type == FavoriteType.bundle:
            bundle = get_bundle_by_id(db, fav.target_id)
            if bundle:
                items.append(FavoriteOut.model_validate(bundle))
        elif target_type == FavoriteType.supplier:
            supplier = get_supplier_by_id(db, fav.target_id)
            if supplier:
                items.append(FavoriteOut.model_validate(supplier))

    return FavoriteListResponse(items=items)