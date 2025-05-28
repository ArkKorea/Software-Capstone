from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from enum import Enum as PyEnum
from typing import List

from app.models.base import Base

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
    registered_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    allergen: Mapped[List['Allergen']] = relationship('Allergen', secondary='food_allergens', back_populates='food')

    supplier: Mapped['Supplier'] = relationship("Supplier", back_populates="foods")
    registered_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    bundles: Mapped[List['FoodBundle']] = relationship("FoodBundle", secondary="food_bundle_items", back_populates="items")
    barcode: Mapped['Barcode'] = relationship('Barcode', back_populates='food')
    qr_link: Mapped['QrLink'] = relationship('QrLink', back_populates='food')
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="food")
    food_bundle_items: Mapped[List['FoodBundleItem']] = relationship('FoodBundleItem', back_populates='food')
    intake_logs: Mapped[List['IntakeLog']] = relationship("IntakeLog", back_populates="food")
