from sqlalchemy.orm import Session
from app.models.favorite import Favorite, FavoriteType
from app.models.food import Food
from app.models.food_bundle import FoodBundle
from app.models.supplier import Supplier

# 즐겨찾기 추가
def add_favorite(db: Session, user_id: int, target_type: FavoriteType, target_id: int) -> Favorite:
    favorite = Favorite(
        user_id=user_id,
        type=target_type,
        target_id=target_id,
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite

# 즐겨찾기 삭제
def remove_favorite(db: Session, user_id: int, target_type: FavoriteType, target_id: int) -> bool:
    favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.type == target_type,
        Favorite.target_id == target_id
    ).first()

    if not favorite:
        return False

    db.delete(favorite)
    db.commit()
    return True

# 단품(food) 조회
def get_food_by_id(db: Session, food_id: int) -> Food | None:
    return db.query(Food).filter(Food.id == food_id).first()

# 번들(bundle) 조회
def get_bundle_by_id(db: Session, bundle_id: int) -> FoodBundle | None:
    return db.query(FoodBundle).filter(FoodBundle.id == bundle_id).first()

# 공급자(supplier) 조회
def get_supplier_by_id(db: Session, supplier_id: int) -> Supplier | None:
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

# 즐겨찾기 조회
def get_favorites_by_type(db: Session, user_id: int, target_type: FavoriteType) -> list[Favorite]:
    return db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.type == target_type
    ).order_by(Favorite.id.desc())

# 중복 검사
def get_favorite_by_type_and_target(db: Session, user_id: int, target_type: FavoriteType, target_id: int) -> Favorite | None:
    return db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.type == target_type,
        Favorite.target_id == target_id
    ).first()
