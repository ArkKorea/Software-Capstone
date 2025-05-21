import os
import base64
import uuid
from app.schemas.product import ProductCreate
from app.models.user import User

from app.crud.product import *
from app.schemas.product import ProductResponse, BundleResponse, ProductCreateResponse
from app.models.food import Food
from app.models.user import User
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

UPLOAD_DIR = "app/static/images/products" # 로컬 테스트 용도
os.makedirs(UPLOAD_DIR, exist_ok=True)

def decode_barcode(value: str, db: Session, current_user: User) -> ProductResponse:
    product = get_product_by_barcode(value, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return build_product_response(product, current_user)

def decode_qrcode(value: str, db: Session, current_user: User):
    data_type = get_type_by_qrcode(value, db)
    if data_type == 'food':
        product = get_product_by_qrcode(value, db)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return build_product_response(product, current_user)
    elif data_type == 'bundle':
        bundle = get_bundle_by_qrcode(value, db)
        if not bundle:
            raise HTTPException(status_code=404, detail="Product not found")
        return BundleResponse(
            bundle_id=bundle.id,
            name=bundle.name,
            image_url=bundle.image_url,
            product_list=[
                build_product_response(f) for f in bundle.items
            ]
        )
    elif data_type == 'supplier':
        supplier = get_supplier_by_qrcode(value, db)
        if not supplier:
            raise HTTPException(status_code=404, detail="등록된 매장이 없습니다.")
        return RedirectResponse(url=f"/supplier/{supplier.id}")
    else:
        raise HTTPException(status_code=400, detail="유효하지 않은 요청 타입입니다. 'barcode' 또는 'qrcode'를 입력해주세요.")

def build_product_response(product: Food, current_user: User) -> ProductResponse:
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_allergen_ids = [a.id for a in getattr(current_user, "allergen", [])]
    return ProductResponse(
        product_id=product.id,
        name=product.name,
        image_url=product.image_url or "",
        allergen_hit=[a.name for a in product.allergen if a.id in user_allergen_ids],
        allergen_safe=[a.name for a in product.allergen if a.id not in user_allergen_ids],
        ingredient_text=product.ingredient or "",
        is_favorite=any(f.user_id == current_user.id for f in product.favorites),
        supplier_id=product.supplier_id,
        supplier_name=product.supplier.name
    )

def save_image_from_base64(base64_str: str) -> str:
    try:
        image_data = base64.b64decode(base64_str)
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(image_data)
        return f"/static/images/products/{filename}"
    except Exception:
        raise HTTPException(status_code=400, detail="이미지 인코딩이 잘못되었습니다.")

# 제품 등록록
def create_product_service(db: Session, product: ProductCreate, user: User) -> ProductCreateResponse:
    supplier_id = user.supplier_id if user.supplier_id else 1

    image_url = None
    if product.image_base64:
        image_url = save_image_from_base64(product.image_base64)

    food = create_product(
        db=db,
        product=product,
        supplier_id=supplier_id,
        registered_by_user_id=user.id,
        image_url=image_url or ""
    )

    return ProductCreateResponse(
        product_id=food.id,
        name=food.name,
        image_url=food.image_url or "",
        ingredient=food.ingredient or "",
        supplier_id=food.supplier.id,
        supplier_name=food.supplier.name
    )
