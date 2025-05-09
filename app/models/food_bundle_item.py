from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from enum import Enum as PyEnum
from typing import List
from app.models.base import Base
from app.models.food import Food
from app.models.food_bundle import FoodBundle

class FoodBundleItem(Base):
    __tablename__ = "food_bundle_items"

    bundle_id: Mapped[int] = mapped_column(ForeignKey("food_bundles.id"), primary_key=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"), primary_key=True)

    bundle: Mapped['FoodBundle'] = relationship("FoodBundle", back_populates="items")
    food: Mapped[List['Food']] = relationship("Food", back_populates="bundles")
