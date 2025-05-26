import os
import base64
import uuid
from app.schemas.product import ProductCreate
from app.crud.product import create_product
from app.models.user import User

from app.crud.product import *
from app.schemas.product import ProductResponse, BundleResponse, ProductCreateResponse, ProductUpdate, ProductDelete
from app.schemas.supplier import SupplierDetailResponse
from app.models.food import Food
from app.models.user import User
from app.models.food_allergens import FoodAllergen
from app.models.allergen import Allergen
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import delete
from typing import Union
from app.services.detail_service import get_bundle_detail_service, get_product_detail_service

UPLOAD_DIR = "app/static/images/products" # 로컬 테스트 용도
os.makedirs(UPLOAD_DIR, exist_ok=True)

def decode_barcode(value: str, db: Session) -> RedirectResponse:
    product = get_product_by_barcode(value, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return RedirectResponse(url=f"/api/detail/product/{product.id}", status_code=303)

def decode_qrcode(value: str, db: Session) -> RedirectResponse:
    data_type = get_type_by_qrcode(value, db)
    if data_type == 'food':
        product = get_product_by_qrcode(value, db)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return RedirectResponse(url=f"/api/detail/product/{product.id}", status_code=303)

    elif data_type == 'bundle':
        bundle = get_bundle_by_qrcode(value, db)
        if not bundle:
            raise HTTPException(status_code=404, detail="Product not found")
        return RedirectResponse(url=f"/api/detail/bundle/{bundle.id}", status_code=303)

    elif data_type == 'supplier':
        supplier = get_supplier_by_qrcode(value, db)
        if not supplier:
            raise HTTPException(status_code=404, detail="등록된 매장이 없습니다.")
        return RedirectResponse(url=f"/api/detail/supplier/{supplier.id}", status_code=303)

    else:
        raise HTTPException(status_code=400, detail="유효하지 않은 요청 타입입니다. 'barcode' 또는 'qrcode'를 입력해주세요.")

def build_product_response(product: Food, current_user: User) -> ProductResponse:
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_allergen_ids = [a.id for a in getattr(current_user, "allergen", [])]
    return ProductResponse(
        product_id=product.id,
        name=product.name or "",
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

# 제품 등록
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

# 내 제품 목록 조회
def get_my_products_service(db: Session, user: User) -> list[ProductResponse]:
    if user.role != "supplier" or not user.supplier_id:
        raise HTTPException(status_code=403, detail="상품 목록 조회 권한이 없습니다.")

    products = db.query(Food).filter(Food.supplier_id == user.supplier_id).all()

    result = []
    for food in products:
        allergens = [a.name for a in food.allergen]
        result.append(ProductResponse(
            product_id=food.id,
            name=food.name,
            image_url=food.image_url or "",
            ingredient=food.ingredient or "",
            allergen_hit=allergens,
            allergen_safe=[],
            is_favorite=False,
            supplier_id=user.supplier_id,
            supplier_name=user.name
        ))
    return result

# 내 상품 수정
def update_product_service(db: Session, data: ProductUpdate, user: User):
    if user.role != "supplier" or not user.supplier_id:
        raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")

    product = db.query(Food).filter(Food.id == data.product_id, Food.supplier_id == user.supplier_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="해당 상품을 찾을 수 없습니다.")

    if data.name:
        product.name = data.name
    if data.ingredient is not None:
        product.ingredient = data.ingredient
    if data.image_base64:
        product.image_url = save_image_from_base64(data.image_base64)

    # 알러지 정보 갱신
    if data.allergies is not None:
        db.execute(delete(FoodAllergen).where(FoodAllergen.food_id == product.id))

        allergen_objs = db.query(Allergen).filter(Allergen.name.in_(data.allergies)).all()
        for allergen in allergen_objs:
            db.add(FoodAllergen(food_id=product.id, allergen_id=allergen.id))

    db.commit()
    return {"message": "상품이 성공적으로 수정되었습니다."}

# 내 제품 삭제
def delete_product_service(db: Session, data: ProductDelete, user: User):
    if user.role != "supplier" or not user.supplier_id:
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")

    product = db.query(Food).filter(
        Food.id == data.product_id,
        Food.supplier_id == user.supplier_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="해당 상품을 찾을 수 없습니다.")

    db.delete(product)
    db.commit()

    return {"message": "상품이 성공적으로 삭제되었습니다."}