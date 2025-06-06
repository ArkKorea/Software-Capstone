from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.models.base import Base
from typing import Optional

class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    food_id: Mapped[Optional[int]] = mapped_column(ForeignKey("foods.id", ondelete="CASCADE"), nullable=True)
    bundle_id: Mapped[Optional[int]] = mapped_column(ForeignKey("food_bundles.id", ondelete="CASCADE"), nullable=True)
    supplier_id: Mapped[Optional[int]] = mapped_column(ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    food: Mapped[Optional["Food"]] = relationship("Food", back_populates="favorites")
    bundle: Mapped[Optional["FoodBundle"]] = relationship("FoodBundle", back_populates="favorites")
    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="favorites")