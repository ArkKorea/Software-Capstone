from sqlalchemy.orm import Session
from app.models.supplier import Supplier
from app.models.food import Food
from app.models.food_bundle import FoodBundle

def get_store_by_keyword(keyword: str, db: Session):
    return db.query(Supplier).filter(Supplier.name.ilike(f"%{keyword}%")).all()

def get_product_by_keyword(keyword: str, db: Session):
    return db.query(Food).filter(Food.name.ilike(f"%{keyword}%")).all()

def get_bundle_by_keyword(keyword: str, db: Session):
    return db.query(FoodBundle).filter(FoodBundle.name.ilike(f"%{keyword}%")).all()

def get_store_by_id(store_id: int, db: Session):
    return db.query(Supplier).filter(Supplier.id == store_id).first()