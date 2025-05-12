from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models.base import Base

user_allergens = Table(
    'user_allergens', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('allergen_id', Integer, ForeignKey('allergens.id', ondelete='CASCADE'), primary_key=True)
)
