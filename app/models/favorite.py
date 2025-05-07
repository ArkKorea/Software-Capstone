from sqlalchemy import Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import enum
from app.models.base import Base

class FavoriteType(str, enum.Enum):
    food = "food"
    bundle = "bundle"
    supplier = "supplier"

class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    type: Mapped[FavoriteType]  # 'food' | 'bundle' | 'supplier'
    target_id: Mapped[int]
