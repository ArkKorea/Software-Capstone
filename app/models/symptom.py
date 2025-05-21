from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class SymptomsLog(Base):
    __tablename__ = 'symptoms_log'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=False)
    skin: Mapped[int] = mapped_column(Integer)
    stomach: Mapped[int] = mapped_column(Integer)
    breath: Mapped[int] = mapped_column(Integer)
    headache: Mapped[int] = mapped_column(Integer)
    fatigue: Mapped[int] = mapped_column(Integer)
    log_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[Optional['User']] = relationship('User', back_populates='symptoms_logs')