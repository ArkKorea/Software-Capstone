from pydantic import BaseModel
from enum import Enum
from typing import List, Union
from app.schemas.food import FoodOut
from app.schemas.supplier import SupplierOut
from app.schemas.food_bundle import FoodBundleOut

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

class FavoriteListResponse(BaseModel):
    items: List[Union[FoodOut, SupplierOut, FoodBundleOut]]
