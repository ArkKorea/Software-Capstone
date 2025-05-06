from sqlalchemy.orm import Session
from app.models.models import Foods, FoodBundles, Suppliers

def get_store_by_keyword(keyword: str, db: Session):
    return db.query(Suppliers).filter(Suppliers.name.ilike(f"%{keyword}%")).all()

def get_product_by_keyword(keyword: str, db: Session):
    return db.query(Foods).filter(Foods.name.ilike(f"%{keyword}%")).all()

def get_bundle_by_keyword(keyword: str, db: Session):
    return db.query(FoodBundles).filter(FoodBundles.name.ilike(f"%{keyword}%")).all()

def get_store_by_id(store_id: int, db: Session):
    return db.query(Suppliers).filter(Suppliers.id == store_id).first()