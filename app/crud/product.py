from sqlalchemy.orm import Session
from app.models.models import Barcodes, QrLinks
from app.models.food import Food
from app.models.food_bundle import FoodBundle
from app.models.supplier import Supplier

def get_product_by_barcode(barcode: str, db: Session):
    return db.query(Food).filter(Food.barcodes.any(Barcodes.code == barcode)).first()

def get_type_by_qrcode(qrcode: str, db: Session):
    return db.query(QrLinks).filter(QrLinks.code == qrcode).first().type

def get_product_by_qrcode(qrcode: str, db: Session):
    return db.query(Food).filter(Food.qr_links.any(QrLinks.code == qrcode)).first()

def get_bundle_by_qrcode(qrcode: str, db: Session):
    return db.query(FoodBundle).filter(FoodBundle.qr_links.any(QrLinks.code == qrcode)).first()

def get_supplier_by_qrcode(qrcode: str, db: Session):
    return db.query(Supplier).filter(Supplier.qr_links.any(QrLinks.code == qrcode)).first()