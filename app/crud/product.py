from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.models import Barcodes, QrLinks
from app.models.food import Food
from app.models.food_bundle import FoodBundle
from app.models.supplier import Supplier
from app.models.food_allergens import FoodAllergen
from app.schemas.product import ProductCreate

from app.models.allergen import Allergen
import datetime

def get_product_by_barcode(barcode: str, db: Session):
    return db.query(Food).filter(Food.barcode.any(Barcodes.code == barcode)).first()

def get_type_by_qrcode(qrcode: str, db: Session):
    return db.query(QrLinks).filter(QrLinks.code == qrcode).first().type

def get_product_by_qrcode(qrcode: str, db: Session):
    return db.query(Food).filter(Food.qr_link.any(QrLinks.code == qrcode)).first()

def get_bundle_by_qrcode(qrcode: str, db: Session):
    return db.query(FoodBundle).filter(FoodBundle.qr_link.any(QrLinks.code == qrcode)).first()

def get_supplier_by_qrcode(qrcode: str, db: Session):
    return db.query(Supplier).filter(Supplier.qr_link.any(QrLinks.code == qrcode)).first()

def get_product_by_id(product_id: int, db: Session):
    return db.query(Food).filter(Food.id == product_id).first()

def get_product_by_name(product_name: str, db: Session):
    return db.query(Food).filter(Food.name == product_name).first()

def get_all_products_id_name(db: Session):
    return db.query(Food.id, Food.name).all()

# 제품 생성
def create_product(
    db: Session,
    product: ProductCreate,
    supplier_id: int,
    registered_by_user_id: int,
    image_url: str
) -> Food:
    # 1. Food 생성
    new_food = Food(
        name=product.name,
        ingredient=product.ingredient,
        image_url=image_url,
        source_type="user",
        supplier_id=supplier_id,
        registered_by_user_id=registered_by_user_id,
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_food)
    db.flush()  # food.id 확보용

    # 2. 알러지 이름 → id 매핑
    stmt = select(Allergen).where(Allergen.name.in_(product.allergies))
    allergen_objs = db.scalars(stmt).all()

    for allergen in allergen_objs:
        db.add(FoodAllergen(food_id=new_food.id, allergen_id=allergen.id))

    db.commit()
    db.refresh(new_food)
    return new_food