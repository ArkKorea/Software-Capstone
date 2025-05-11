from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models.base import Base

food_allergens = Table(
    "food_allergens",
    Base.metadata,
    Column("food_id", Integer, ForeignKey("foods.id", ondelete="CASCADE"), primary_key=True),
    Column("allergen_id", Integer, ForeignKey("allergens.id", ondelete="CASCADE"), primary_key=True),
)