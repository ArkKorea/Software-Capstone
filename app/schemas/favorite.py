from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class FavoriteType(str, Enum):
    food = "food"
    bundle = "bundle"
    supplier = "supplier"

class FavoriteActionRequest(BaseModel):
    type: FavoriteType
    target_id: int
    action: str  # "add" or "remove"

class FavoriteOut(BaseModel):
    target_id: int
    created_at: datetime

class FavoriteListResponse(BaseModel):
    items: list[FavoriteOut]
