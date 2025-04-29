
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.favorite import FavoriteType
from app.crud.favorite import (
    add_favorite,
    remove_favorite,
    get_favorites_by_type
)
from app.schemas.favorite import FavoriteActionRequest, FavoriteListResponse, FavoriteOut

# 즐겨찾기 추가/삭제
def toggle_favorite(request: FavoriteActionRequest, user_id: int, db: Session) -> str:
    if request.action == "add":
        add_favorite(db, user_id, request.type, request.target_id)
        return "즐겨찾기가 추가되었습니다."
    elif request.action == "remove":
        removed = remove_favorite(db, user_id, request.type, request.target_id)
        if not removed:
            raise HTTPException(status_code=404, detail="해당 즐겨찾기를 찾을 수 없습니다.")
        return "즐겨찾기가 삭제되었습니다."
    else:
        raise HTTPException(status_code=400, detail="유효하지 않은 요청입니다.")

# 즐겨찾기 목록 조회
def get_favorites(user_id: int, target_type: FavoriteType, db: Session) -> FavoriteListResponse:
    favorites = get_favorites_by_type(db, user_id, target_type)
    items = [FavoriteOut(target_id=f.target_id, created_at=f.created_at) for f in favorites]
    return FavoriteListResponse(items=items)
