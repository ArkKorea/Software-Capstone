from sqlalchemy.orm import Session
from app.models.favorite import Favorite
from app.models.food import Food
from app.models.food_bundle import FoodBundle
from app.models.supplier import Supplier

# 즐겨찾기 추가
def add_favorite(db: Session, user_id: int, food_id: int = None, bundle_id: int = None, supplier_id: int = None) -> Favorite:
    if sum([food_id is not None, bundle_id is not None, supplier_id is not None]) != 1:
        raise ValueError("Exactly one of food_id, bundle_id, or supplier_id must be provided.")

    favorite = Favorite(
        user_id=user_id,
        food_id=food_id,
        bundle_id=bundle_id,
        supplier_id=supplier_id
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite

# 즐겨찾기 삭제
def remove_favorite(db: Session, user_id: int, food_id: int = None, bundle_id: int = None, supplier_id: int = None) -> bool:
    if sum([food_id is not None, bundle_id is not None, supplier_id is not None]) != 1:
        raise ValueError("Exactly one of food_id, bundle_id, or supplier_id must be provided.")

    favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.food_id == food_id,
        Favorite.bundle_id == bundle_id,
        Favorite.supplier_id == supplier_id,
    ).first()

    if not favorite:
        return False

    db.delete(favorite)
    db.commit()
    return True

# 즐겨찾기 조회 (food/bundle/supplier 모두 포함)
def get_favorites(db: Session, user_id: int) -> list[Favorite]:
    return db.query(Favorite).filter(
        Favorite.user_id == user_id
    ).order_by(Favorite.id.desc()).all()

# 중복 검사
def get_favorite_by_target(db: Session, user_id: int, food_id: int = None, bundle_id: int = None, supplier_id: int = None) -> Favorite | None:
    return db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.food_id == food_id,
        Favorite.bundle_id == bundle_id,
        Favorite.supplier_id == supplier_id
    ).first()
