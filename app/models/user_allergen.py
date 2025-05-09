from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase

user_allergens = Table(
    'user_allergens', DeclarativeBase.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('allergen_id', Integer, ForeignKey('allergens.id', ondelete='CASCADE'), primary_key=True)
)
