from app.crud.product import *
from app.core.auth import get_current_user
from app.schemas.product import ProductResponse, BundleResponse
from app.models.food import Food
from app.models.user import User
from fastapi import HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session


def decode_barcode(value: str, db: Session) -> ProductResponse:
    product = get_product_by_barcode(value, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return build_product_response(product,  db)

def decode_qrcode(value: str, db: Session):
    data_type = get_type_by_qrcode(value, db)
    if data_type == 'food':
        product = get_product_by_qrcode(value, db)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return build_product_response(product)
    elif data_type == 'bundle':
        bundle = get_bundle_by_qrcode(value, db)
        if not bundle:
            raise HTTPException(status_code=404, detail="Product not found")
        return BundleResponse(
            bundle_id=bundle.id,
            name=bundle.name,
            image_url=bundle.image_url,
            product_list=[
                build_product_response(f) for f in bundle.food
            ]
        )
    elif data_type == 'supplier':
        supplier = get_supplier_by_qrcode(value, db)
        if not supplier:
            raise HTTPException(status_code=404, detail="등록된 매장이 없습니다.")
        return RedirectResponse(url=f"/supplier/{supplier.id}")
    else:
        raise HTTPException(status_code=400, detail="유효하지 않은 요청 타입입니다. 'barcode' 또는 'qrcode'를 입력해주세요.")

def build_product_response(product: Food, current_user: User = Depends(get_current_user)) -> ProductResponse:
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return ProductResponse(
        product_id=product.id,
        name=product.name,
        image_url=product.image_url,
        allergen_hit=[a.id for a in product.allergen if a.id in current_user.allergen],
        allergen_safe=[a.id for a in product.allergen if a.id not in current_user.allergen],
        ingredient_text=product.ingredient,
        is_favorite=any(f.user_id == current_user.id for f in product.favorites),
        supplier_id=product.supplier_id,
        supplier_name=product.supplier.name
    )
