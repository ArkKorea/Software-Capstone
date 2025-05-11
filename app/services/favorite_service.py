from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud.favorite import (
    add_favorite,
    remove_favorite,
    get_favorites,
    get_favorite_by_target,
)
from app.crud.item_lookup import (
    get_food_by_id,
    get_bundle_by_id,
    get_supplier_by_id,
)
from app.schemas.favorite import FavoriteActionRequest, FavoriteListResponse, FavoriteOut

# 즐겨찾기 추가/삭제
def toggle_favorite(request: FavoriteActionRequest, user_id: int, db: Session) -> str:
    food_id = request.food_id
    bundle_id = request.bundle_id
    supplier_id = request.supplier_id

    # 유효성 검사 (정확히 하나만 있어야 함)
    targets = [food_id, bundle_id, supplier_id]
    if sum(x is not None for x in targets) != 1:
        raise HTTPException(status_code=400, detail="food_id, bundle_id, supplier_id 중 하나만 전달해야 합니다.")

    # 실제 객체 존재 여부 확인
    if food_id:
        if not get_food_by_id(db, food_id):
            raise HTTPException(status_code=404, detail="존재하지 않는 단품입니다.")
    elif bundle_id:
        if not get_bundle_by_id(db, bundle_id):
            raise HTTPException(status_code=404, detail="존재하지 않는 번들입니다.")
    elif supplier_id:
        if not get_supplier_by_id(db, supplier_id):
            raise HTTPException(status_code=404, detail="존재하지 않는 공급자입니다.")

    # 중복 여부 확인
    existing = get_favorite_by_target(db, user_id, food_id, bundle_id, supplier_id)

    if request.action == "add":
        if existing:
            raise HTTPException(status_code=400, detail="이미 즐겨찾기에 등록된 항목입니다.")
        add_favorite(db, user_id, food_id, bundle_id, supplier_id)
        return "즐겨찾기가 추가되었습니다."

    elif request.action == "remove":
        if not existing:
            raise HTTPException(status_code=404, detail="즐겨찾기 내역이 없습니다.")
        remove_favorite(db, user_id, food_id, bundle_id, supplier_id)
        return "즐겨찾기가 삭제되었습니다."

    else:
        raise HTTPException(status_code=400, detail="유효하지 않은 요청입니다.")


# 즐겨찾기 목록 조회
def get_favorites(user_id: int, db: Session, target: str) -> FavoriteListResponse:
    favorites = get_favorites(db, user_id)
    items = []

    for fav in favorites:
        if target == "food" and fav.food_id:
            food = get_food_by_id(db, fav.food_id)
            if food:
                items.append(FavoriteOut.model_validate(food))
        elif target == "bundle" and fav.bundle_id:
            bundle = get_bundle_by_id(db, fav.bundle_id)
            if bundle:
                items.append(FavoriteOut.model_validate(bundle))
        elif target == "supplier" and fav.supplier_id:
            supplier = get_supplier_by_id(db, fav.supplier_id)
            if supplier:
                items.append(FavoriteOut.model_validate(supplier))

    return FavoriteListResponse(items=items)
