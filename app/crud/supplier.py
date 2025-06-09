from sqlalchemy.orm import Session
from app.models.supplier import Supplier
from typing import Optional

def get_supplier_by_name(db: Session, name: str) -> Optional[Supplier]:
    return db.query(Supplier).filter(Supplier.name == name).first()

def create_supplier(db: Session, name: str) -> Supplier:
    new_supplier = Supplier(name=name)
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier
