from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.supplier import SupplierDetailResponse, BundleSummary
from app.schemas.product import ProductResponse, BundleResponse
from app.crud.item_lookup import get_food_by_id, get_bundle_by_id, get_supplier_by_id
from app.crud.history import add_or_update_view_log

# id를 통한 상품 상세 조회
def get_product_detail_service(db: Session, product_id: int, user: User) -> ProductResponse:
    food = get_food_by_id(db, product_id)
    if not food:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    if user.role in ("consumer", "supplier"):
        add_or_update_view_log(db, user.id, "food", product_id)

    user_allergen_names = {a.name for a in user.allergens} if user.role == "consumer" else set()
    food_allergen_names = {a.name for a in food.allergen}

    allergen_hit = list(user_allergen_names & food_allergen_names)
    allergen_safe = list(food_allergen_names - user_allergen_names)

    return ProductResponse(
        product_id=food.id,
        name=food.name,
        image_url=food.image_url or "",
        ingredient=food.ingredient or "",
        allergen_hit=allergen_hit,
        allergen_safe=allergen_safe,
        is_favorite=False,
        supplier_id=food.supplier.id,
        supplier_name=food.supplier.name
    )

def get_bundle_detail_service(db: Session, bundle_id: int, user: User) -> BundleResponse:
    bundle = get_bundle_by_id(db, bundle_id)
    if not bundle:
        raise HTTPException(status_code=404, detail="묶음 상품을 찾을 수 없습니다.")

    if user.role in ("consumer", "supplier"):
        add_or_update_view_log(db, user.id, "bundle", bundle_id)

    user_allergen_names = {a.name for a in user.allergens} if user.role == "consumer" else set()

    products: list[ProductResponse] = []
    for item in bundle.items:
        food = item.food
        food_allergen_names = {a.name for a in food.allergen}
        allergen_hit = list(user_allergen_names & food_allergen_names)
        allergen_safe = list(food_allergen_names - user_allergen_names)

        products.append(ProductResponse(
            product_id=food.id,
            name=food.name,
            image_url=food.image_url or "",
            ingredient=food.ingredient or "",
            allergen_hit=allergen_hit,
            allergen_safe=allergen_safe,
            is_favorite=False,  # 즐겨찾기 기능 미적용
            supplier_id=food.supplier.id,
            supplier_name=food.supplier.name
        ))

    return BundleResponse(
        id=bundle.id,
        name=bundle.name,
        image_url=bundle.image_url or "",
        supplier_id=bundle.supplier.id,
        products=products
    )

def get_supplier_detail_service(db: Session, supplier_id: int, user: User) -> SupplierDetailResponse:
    supplier = get_supplier_by_id(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="판매자를 찾을 수 없습니다.")

    if user.role in ("consumer", "supplier"):
        add_or_update_view_log(db, user.id, "supplier", supplier_id)

    user_allergen_names = {a.name for a in user.allergens} if user.role == "consumer" else set()

    # 상품 목록 구성
    products = []
    for food in supplier.foods:
        food_allergen_names = {a.name for a in food.allergen}
        allergen_hit = list(user_allergen_names & food_allergen_names)
        allergen_safe = list(food_allergen_names - user_allergen_names)

        products.append(ProductResponse(
            product_id=food.id,
            name=food.name,
            image_url=food.image_url or "",
            ingredient=food.ingredient or "",
            allergen_hit=allergen_hit,
            allergen_safe=allergen_safe,
            is_favorite=False,
            supplier_id=supplier.id,
            supplier_name=supplier.name
        ))

    # 번들 요약 구성
    bundles = [
        BundleSummary(
            id=bundle.id,
            name=bundle.name,
            image_url=bundle.image_url or ""
        )
        for bundle in supplier.bundles
    ]

    return SupplierDetailResponse(
        id=supplier.id,
        name=supplier.name,
        image_url=supplier.image_url or "",
        products=products,
        bundles=bundles
    )
