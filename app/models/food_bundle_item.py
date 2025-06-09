from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.base import Base

class FoodBundleItem(Base):
    __tablename__ = "food_bundle_items"

    bundle_id: Mapped[int] = mapped_column(ForeignKey("food_bundles.id"), primary_key=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"), primary_key=True)

    bundle: Mapped['FoodBundle'] = relationship("FoodBundle", back_populates="food_bundle_items")
    food: Mapped['Food'] = relationship("Food", back_populates="food_bundle_items")
