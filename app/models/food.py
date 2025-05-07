from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from enum import Enum as PyEnum

from app.models.base import Base

from app.models.food_bundle_item import FoodBundleItem


class SourceType(PyEnum):
    user = "user"
    ocr = "ocr"
    crowl = "crowl"
    
class Food(Base):
    __tablename__ = "foods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    ingredient: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(255))
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    supplier = relationship("Supplier", back_populates="foods")
    bundles = relationship("FoodBundleItem", back_populates="food")
