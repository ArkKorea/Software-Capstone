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
from app.schemas.search import SearchProductResponse, Bundle, SearchStoreResponse, Store
from app.models.user import User
from app.services.detail_service import get_product_detail_service

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
def get_favorite_items(db: Session, current_user: User) -> SearchProductResponse:
    favorites = get_favorites(db, current_user.id)

    # 1. Product 즐겨찾기 수집
    favorite_products = [
        get_product_detail_service(db, fav.food_id, current_user)
        for fav in favorites if fav.food_id
    ]

    # 2. Bundle 즐겨찾기 수집
    favorite_bundles = []
    user_allergen_ids = [a.id for a in current_user.allergen]

    for fav in favorites:
        if not fav.bundle_id:
            continue

        bundle = get_bundle_by_id(db, fav.bundle_id)
        if not bundle:
            continue

        allergen_hit = []
        allergen_safe = []

        for product in bundle.items:
            allergen_hit += [a.name for a in product.allergen if a.id in user_allergen_ids]
            allergen_safe += [a.name for a in product.allergen if a.id not in user_allergen_ids]

        favorite_bundles.append(Bundle(
            bundle_id=bundle.id,
            name=bundle.name,
            image_url=bundle.image_url or "",
            allergen_hit=list(set(allergen_hit)),
            allergen_safe=list(set(allergen_safe)),
            supplier_id=bundle.supplier.id,
            supplier_name=bundle.supplier.name,
            is_favorite=True
        ))

    return SearchProductResponse(products=favorite_products, bundles=favorite_bundles)

def get_favorite_suppliers(db: Session, current_user: User) -> SearchStoreResponse:
    favorites = get_favorites(db, current_user.id)

    stores = []
    for fav in favorites:
        if not fav.supplier_id:
            continue
        supplier = get_supplier_by_id(db, fav.supplier_id)
        if not supplier:
            continue
        stores.append(Store(
            store_id=supplier.id,
            name=supplier.name,
            address=supplier.address or "",
            is_favorite=True
        ))

    return SearchStoreResponse(stores=stores)