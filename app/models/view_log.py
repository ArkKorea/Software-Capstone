import datetime
from typing import Optional
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.enums import FavoriteType

class ViewLog(Base):
    __tablename__ = "view_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    type: Mapped[FavoriteType]

    food_id: Mapped[Optional[int]] = mapped_column(ForeignKey("foods.id", ondelete="CASCADE"), nullable=True)
    bundle_id: Mapped[Optional[int]] = mapped_column(ForeignKey("food_bundles.id", ondelete="CASCADE"), nullable=True)
    supplier_id: Mapped[Optional[int]] = mapped_column(ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=True)

    viewed_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="view_logs")
    food = relationship("Food", lazy="joined")
    bundle = relationship("FoodBundle", lazy="joined")
    supplier = relationship("Supplier", lazy="joined")
