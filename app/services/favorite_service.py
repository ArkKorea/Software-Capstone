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
from app.schemas.search import SearchProductResponse, Bundle, SearchStoreResponse, Store, StoreWithProductsResponse, StoreProductListResponse
from app.models.user import User
from app.services.detail_service import get_product_detail_service
from app.models.food import Food

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

def get_favorite_suppliers_with_products(db: Session, current_user: User) -> StoreWithProductsResponse:
    favorites = get_favorites(db, current_user.id)

    store_responses = []
    visited_supplier_ids = set()

    for fav in favorites:
        supplier_id = fav.supplier_id
        if not supplier_id or supplier_id in visited_supplier_ids:
            continue

        supplier = get_supplier_by_id(db, supplier_id)
        if not supplier:
            continue

        visited_supplier_ids.add(supplier_id)

        # 매장 정보
        store = Store(
            store_id=supplier.id,
            name=supplier.name,
            address=supplier.address or "",
            is_favorite=True
        )

        # 해당 매장의 모든 상품 조회
        foods = (
            db.query(Food)
            .filter(Food.supplier_id == supplier.id)
            .all()
        )

        # ProductResponse로 가공
        product_responses = [
            get_product_detail_service(db, food.id, current_user)
            for food in foods
        ]

        # Store + 상품 리스트 추가
        store_responses.append(
            StoreProductListResponse(
                store=store,
                products=product_responses
            )
        )

    return StoreWithProductsResponse(stores=store_responses)