from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
class IntakeLog(Base):
    __tablename__ = "intake_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    food_name: Mapped[str] = mapped_column(String(255), nullable=False)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id", ondelete="CASCADE"), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    memo: Mapped[Text] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow,nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="intake_logs")
    food: Mapped["Food"] = relationship("Food", back_populates="intake_logs")
