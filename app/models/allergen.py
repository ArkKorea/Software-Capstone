from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base

from app.models.user_allergen import user_allergens
from typing import List
class Allergen(Base):
    __tablename__ = 'allergens'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    food: Mapped[List['Food']] = relationship('Food', back_populates='allergen')
    user: Mapped[List['User']]= relationship('User',secondary=user_allergens, back_populates='allergen')