from sqlalchemy.orm import Session
from app.models.favorite import Favorite, FavoriteType
from datetime import datetime

# 즐겨찾기 추가가
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

# 즐겨찾기 조회
def get_favorites_by_type(db: Session, user_id: int, target_type: FavoriteType) -> list[Favorite]:
    return db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.type == target_type
    ).order_by(Favorite.id.desc())

# 중복 검사사
def get_favorite_by_type_and_target(db: Session, user_id: int, target_type: FavoriteType, target_id: int) -> Favorite | None:
    return db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.type == target_type,
        Favorite.target_id == target_id
    ).first()
