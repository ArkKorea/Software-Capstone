from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from sqlalchemy import String, Boolean, Date, Integer, Enum, DateTime
from datetime import date, datetime
import enum
from app.models.base import Base
from .user_allergen import user_allergens

class RoleEnum(enum.Enum):
    consumer = "consumer"
    supplier = "supplier"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    birth: Mapped[date] = mapped_column(Date)
    role: Mapped[RoleEnum]
    supplier_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verification_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    social_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    social_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    terms_version_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    reset_password_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reset_password_expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    allergen = relationship('Allergen',secondary=user_allergens, back_populates='user')
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="user", cascade="all, delete")
    view_logs: Mapped[List["ViewLog"]] = relationship("ViewLog", back_populates="user")
