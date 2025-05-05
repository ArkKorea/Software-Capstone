from sqlalchemy.orm import Session
from app.models.models import Foods, Barcodes, QrLinks, FoodBundles, Suppliers

def get_product_by_barcode(barcode: str, db: Session):
    return db.query(Foods).filter(Foods.barcodes.any(Barcodes.code == barcode)).first()

def get_type_by_qrcode(qrcode: str, db: Session):
    return db.query(QrLinks).filter(QrLinks.code == qrcode).first().type

def get_product_by_qrcode(qrcode: str, db: Session):
    return db.query(Foods).filter(Foods.qr_links.any(QrLinks.code == qrcode)).first()

def get_bundle_by_qrcode(qrcode: str, db: Session):
    return db.query(FoodBundles).filter(FoodBundles.qr_links.any(QrLinks.code == qrcode)).first()

def get_supplier_by_qrcode(qrcode: str, db: Session):
    return db.query(Suppliers).filter(Suppliers.qr_links.any(QrLinks.code == qrcode)).first()