from sqlalchemy import Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
from app.models.enums import FavoriteType
from typing import List
from app.models.base import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    type: Mapped[FavoriteType]  # 'food' | 'bundle' | 'supplier'
    target_id: Mapped[int]

    user: Mapped[List['User']] = relationship('User', back_populates='favorites')