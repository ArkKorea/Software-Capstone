from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from enum import Enum as PyEnum
from app.models.base import Base
from typing import List
from app.models.food_bundle_item import FoodBundleItem
from app.models.supplier import Supplier
from app.models.qr_link import QrLink
from .food import Food
class FoodBundle(Base):
    __tablename__ = "food_bundles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    supplier: Mapped['Supplier'] = relationship("Supplier", back_populates="bundles")
    items: Mapped[List['Food']] = relationship("Food", back_populates="bundles")
    qr_link: Mapped['QrLink'] = relationship('QrLink', back_populates='bundle')
