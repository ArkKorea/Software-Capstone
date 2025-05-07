from typing import List, Optional
from sqlalchemy import Column, Date, DateTime, Enum, ForeignKeyConstraint, Index, Integer, String, Table, Text, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Allergens(Base):
    __tablename__ = 'allergens'
    __table_args__ = (
        Index('idx_name', 'name'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    food: Mapped[List['Foods']] = relationship('Foods', secondary='food_allergens', back_populates='allergen')
    user: Mapped[List['Users']] = relationship('Users', secondary='user_allergens', back_populates='allergen')


class Suppliers(Base):
    __tablename__ = 'suppliers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    contact_email: Mapped[Optional[str]] = mapped_column(String(255))
    address: Mapped[Optional[str]] = mapped_column(String(255))
    business_license_number: Mapped[Optional[str]] = mapped_column(String(100))
    is_verified: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))
    image_url: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    food_bundles: Mapped[List['FoodBundles']] = relationship('FoodBundles', back_populates='supplier')
    foods: Mapped[List['Foods']] = relationship('Foods', back_populates='supplier')
    users: Mapped[List['Users']] = relationship('Users', back_populates='supplier')
    favorites: Mapped[List['Favorites']] = relationship('Favorites', back_populates='supplier')
    qr_links: Mapped[List['QrLinks']] = relationship('QrLinks', back_populates='supplier')


class TermsVersions(Base):
    __tablename__ = 'terms_versions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    is_active: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'1'"))

    users: Mapped[List['Users']] = relationship('Users', back_populates='terms_version')


class FoodBundles(Base):
    __tablename__ = 'food_bundles'
    __table_args__ = (
        ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ondelete='CASCADE', name='food_bundles_ibfk_1'),
        Index('idx_supplier_id', 'supplier_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    supplier_id: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    supplier: Mapped['Suppliers'] = relationship('Suppliers', back_populates='food_bundles')
    food: Mapped[List['Foods']] = relationship('Foods', secondary='food_bundle_items', back_populates='bundle')
    favorites: Mapped[List['Favorites']] = relationship('Favorites', back_populates='bundle')
    qr_links: Mapped[List['QrLinks']] = relationship('QrLinks', back_populates='bundle')


class Foods(Base):
    __tablename__ = 'foods'
    __table_args__ = (
        ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ondelete='CASCADE', name='foods_ibfk_1'),
        Index('idx_supplier_id', 'supplier_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    supplier_id: Mapped[int] = mapped_column(Integer)
    ingredient: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(String(255))
    source_type: Mapped[Optional[str]] = mapped_column(Enum('user', 'ocr', 'crowl'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    allergen: Mapped[List['Allergens']] = relationship('Allergens', secondary='food_allergens', back_populates='food')
    bundle: Mapped[List['FoodBundles']] = relationship('FoodBundles', secondary='food_bundle_items', back_populates='food')
    supplier: Mapped['Suppliers'] = relationship('Suppliers', back_populates='foods')
    barcodes: Mapped[List['Barcodes']] = relationship('Barcodes', back_populates='food')
    favorites: Mapped[List['Favorites']] = relationship('Favorites', back_populates='food')
    intake_log: Mapped[List['IntakeLog']] = relationship('IntakeLog', back_populates='food')
    qr_links: Mapped[List['QrLinks']] = relationship('QrLinks', back_populates='food')
    view_log: Mapped[List['ViewLog']] = relationship('ViewLog', back_populates='food')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ondelete='SET NULL', name='users_ibfk_1'),
        ForeignKeyConstraint(['terms_version_id'], ['terms_versions.id'], ondelete='SET NULL', name='users_ibfk_2'),
        Index('idx_email', 'email'),
        Index('idx_supplier_id', 'supplier_id'),
        Index('idx_terms_version_id', 'terms_version_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255))
    gender: Mapped[str] = mapped_column(Enum('male', 'female'))
    birth: Mapped[datetime.date] = mapped_column(Date)
    role: Mapped[str] = mapped_column(Enum('consumer', 'supplier', 'admin'))
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(100))
    supplier_id: Mapped[Optional[int]] = mapped_column(Integer)
    is_verified: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))
    email_verification_token: Mapped[Optional[str]] = mapped_column(String(255))
    social_provider: Mapped[Optional[str]] = mapped_column(String(50))
    social_id: Mapped[Optional[str]] = mapped_column(String(255))
    terms_version_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    allergen: Mapped[List['Allergens']] = relationship('Allergens', secondary='user_allergens', back_populates='user')
    supplier: Mapped[Optional['Suppliers']] = relationship('Suppliers', back_populates='users')
    terms_version: Mapped[Optional['TermsVersions']] = relationship('TermsVersions', back_populates='users')
    favorites: Mapped[List['Favorites']] = relationship('Favorites', back_populates='user')
    intake_log: Mapped[List['IntakeLog']] = relationship('IntakeLog', back_populates='user')
    ocr_results: Mapped[List['OcrResults']] = relationship('OcrResults', back_populates='user')
    symptoms_log: Mapped[List['SymptomsLog']] = relationship('SymptomsLog', back_populates='user')
    view_log: Mapped[List['ViewLog']] = relationship('ViewLog', back_populates='user')


class Barcodes(Base):
    __tablename__ = 'barcodes'
    __table_args__ = (
        ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='CASCADE', name='barcodes_ibfk_1'),
        Index('idx_code', 'code'),
        Index('idx_food_id', 'food_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    food_id: Mapped[int] = mapped_column(Integer)
    code: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    food: Mapped['Foods'] = relationship('Foods', back_populates='barcodes')


class Favorites(Base):
    __tablename__ = 'favorites'
    __table_args__ = (
        ForeignKeyConstraint(['bundle_id'], ['food_bundles.id'], ondelete='CASCADE', name='favorites_ibfk_3'),
        ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='CASCADE', name='favorites_ibfk_2'),
        ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ondelete='CASCADE', name='favorites_ibfk_4'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='favorites_ibfk_1'),
        Index('idx_bundle_id', 'bundle_id'),
        Index('idx_food_id', 'food_id'),
        Index('idx_supplier_id', 'supplier_id'),
        Index('idx_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(Enum('food', 'bundle', 'supplier'))
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    food_id: Mapped[Optional[int]] = mapped_column(Integer)
    bundle_id: Mapped[Optional[int]] = mapped_column(Integer)
    supplier_id: Mapped[Optional[int]] = mapped_column(Integer)

    bundle: Mapped[Optional['FoodBundles']] = relationship('FoodBundles', back_populates='favorites')
    food: Mapped[Optional['Foods']] = relationship('Foods', back_populates='favorites')
    supplier: Mapped[Optional['Suppliers']] = relationship('Suppliers', back_populates='favorites')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='favorites')


t_food_allergens = Table(
    'food_allergens', Base.metadata,
    Column('food_id', Integer, primary_key=True, nullable=False),
    Column('allergen_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['allergen_id'], ['allergens.id'], ondelete='CASCADE', name='food_allergens_ibfk_2'),
    ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='CASCADE', name='food_allergens_ibfk_1'),
    Index('idx_allergen_id', 'allergen_id')
)


t_food_bundle_items = Table(
    'food_bundle_items', Base.metadata,
    Column('bundle_id', Integer, primary_key=True, nullable=False),
    Column('food_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['bundle_id'], ['food_bundles.id'], ondelete='CASCADE', name='food_bundle_items_ibfk_1'),
    ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='CASCADE', name='food_bundle_items_ibfk_2'),
    Index('idx_food_id', 'food_id')
)


class IntakeLog(Base):
    __tablename__ = 'intake_log'
    __table_args__ = (
        ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='SET NULL', name='intake_log_ibfk_2'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='intake_log_ibfk_1'),
        Index('idx_food_id', 'food_id'),
        Index('idx_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    food_id: Mapped[Optional[int]] = mapped_column(Integer)
    intake_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    meal_type: Mapped[Optional[str]] = mapped_column(Enum('breakfast', 'lunch', 'dinner', 'snack'))
    reaction_score: Mapped[Optional[int]] = mapped_column(Integer)

    food: Mapped[Optional['Foods']] = relationship('Foods', back_populates='intake_log')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='intake_log')


class OcrResults(Base):
    __tablename__ = 'ocr_results'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='ocr_results_ibfk_1'),
        Index('idx_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    input_food_name: Mapped[Optional[str]] = mapped_column(String(255))
    suggested_food_name: Mapped[Optional[str]] = mapped_column(String(255))
    uploaded_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='ocr_results')


class QrLinks(Base):
    __tablename__ = 'qr_links'
    __table_args__ = (
        ForeignKeyConstraint(['bundle_id'], ['food_bundles.id'], ondelete='CASCADE', name='fk_bundle'),
        ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='CASCADE', name='fk_food'),
        ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ondelete='CASCADE', name='fk_supplier'),
        Index('idx_code', 'code'),
        Index('fk_bundle', 'bundle_id'),
        Index('fk_food', 'food_id'),
        Index('fk_supplier', 'supplier_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(Enum('food', 'bundle', 'supplier'))
    food_id: Mapped[Optional[int]] = mapped_column(Integer)
    bundle_id: Mapped[Optional[int]] = mapped_column(Integer)
    supplier_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    bundle: Mapped[Optional['FoodBundles']] = relationship('FoodBundles', back_populates='qr_links')
    food: Mapped[Optional['Foods']] = relationship('Foods', back_populates='qr_links')
    supplier: Mapped[Optional['Suppliers']] = relationship('Suppliers', back_populates='qr_links')


class SymptomsLog(Base):
    __tablename__ = 'symptoms_log'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='symptoms_log_ibfk_1'),
        Index('idx_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    log_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    symptoms: Mapped[Optional[str]] = mapped_column(Text)
    severity: Mapped[Optional[int]] = mapped_column(Integer)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='symptoms_log')


t_user_allergens = Table(
    'user_allergens', Base.metadata,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('allergen_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['allergen_id'], ['allergens.id'], ondelete='CASCADE', name='user_allergens_ibfk_2'),
    ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='user_allergens_ibfk_1'),
    Index('idx_allergen_id', 'allergen_id')
)


class ViewLog(Base):
    __tablename__ = 'view_log'
    __table_args__ = (
        ForeignKeyConstraint(['food_id'], ['foods.id'], ondelete='CASCADE', name='view_log_ibfk_2'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='view_log_ibfk_1'),
        Index('idx_food_id', 'food_id'),
        Index('idx_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    food_id: Mapped[Optional[int]] = mapped_column(Integer)
    viewed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    food: Mapped[Optional['Foods']] = relationship('Foods', back_populates='view_log')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='view_log')
