from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from enum import Enum as PyEnum
from app.models.base import Base

class FoodBundle(Base):
    __tablename__ = "food_bundles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    supplier = relationship("Supplier", back_populates="bundles")
    items = relationship("FoodBundleItem", back_populates="bundle")