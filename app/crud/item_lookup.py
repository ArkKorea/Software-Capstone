from sqlalchemy.orm import Session
from app.models.food import Food
from app.models.food_bundle import FoodBundle
from app.models.supplier import Supplier

def get_food_by_id(db: Session, food_id: int) -> Food | None:
    return db.query(Food).filter(Food.id == food_id).first()

def get_bundle_by_id(db: Session, bundle_id: int) -> FoodBundle | None:
    return db.query(FoodBundle).filter(FoodBundle.id == bundle_id).first()

def get_supplier_by_id(db: Session, supplier_id: int) -> Supplier | None:
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()
