from app.models.base import Base
from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from enum import Enum

class typeEnum(Enum):
    food = "food"
    bundle = "bundle"
    suppler = "supplier"

class QrLink(Base):
    __tablename__ = "qr_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[typeEnum]
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"), nullable=True)
    bundle_id: Mapped[int] = mapped_column(ForeignKey("food_bundles.id"), nullable=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    bundle = relationship("FoodBundle", back_populates="qr_link")
    food = relationship("Food", back_populates="qr_link")
    supplier = relationship("Supplier", back_populates="qr_link")