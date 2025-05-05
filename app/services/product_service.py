from app.crud.product import *
from app.crud.user import get_user_by_email
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.schemas.product import ProductResponse, BundleResponse
from app.models.models import Foods, Users


def decode_barcode(value: str, db: Session, user_email:str) -> ProductResponse:
    product = get_product_by_barcode(value, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return build_product_response(product, user_email, db)

def decode_qrcode(value: str, db: Session, user_email:str):
    data_type = get_type_by_qrcode(value, db)
    if data_type == 'food':
        product = get_product_by_qrcode(value, db)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return build_product_response(product, user_email, db)
    elif data_type == 'bundle':
        bundle = get_bundle_by_qrcode(value, db)
        if not bundle:
            raise HTTPException(status_code=404, detail="Bundle not found")
        return BundleResponse(
            bundle_id=bundle.id,
            name=bundle.name,
            image_url=bundle.image_url,
            product_list=[
                build_product_response(f, user_email, db) for f in bundle.food
            ]
        )
    elif data_type == 'supplier':
        supplier = get_supplier_by_qrcode(value, db)
        if not supplier:
            raise HTTPException(status_code=404, detail="등록된 매장이 없습니다.")
        return RedirectResponse(url=f"/supplier/{supplier.id}")
    else:
        raise HTTPException(status_code=400, detail="유효하지 않은 요청 타입입니다. 'barcode' 또는 'qrcode'를 입력해주세요.")

def build_product_response(product: Foods, user_email: str, db: Session) -> ProductResponse:
    user = get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ProductResponse(
        product_id=product.id,
        name=product.name,
        image_url=product.image_url,
        allergen_hit=[a.id for a in product.allergen if a.id in user.allergen],
        allergen_safe=[a.id for a in product.allergen if a.id not in user.allergen],
        ingredient_text=product.ingredient,
        is_favorite=any(f.user_id == user.id for f in product.favorites),
        supplier_id=product.supplier_id,
        supplier_name=product.supplier.name
    )
