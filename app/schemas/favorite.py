from pydantic import BaseModel, field_validator, model_validator
from enum import Enum
from typing import List, Union, Literal, Optional
from app.schemas.food import FoodOut
from app.schemas.supplier import SupplierOut
from app.schemas.food_bundle import FoodBundleOut

class FavoriteType(str, Enum):
    food = "food"
    bundle = "bundle"
    supplier = "supplier"

class FavoriteActionRequest(BaseModel):
    type: FavoriteType
    food_id: Optional[int] = None
    supplier_id: Optional[int] = None
    bundle_id: Optional[int] = None
    action: Literal["add", "remove"]

    @model_validator(mode="after")
    def validate_target_id(self) -> "FavoriteActionRequest":
        if self.type == "food":
            if self.food_id is None or self.supplier_id or self.bundle_id:
                raise ValueError("When type is 'food', only food_id must be set.")
        elif self.type == "supplier":
            if self.supplier_id is None or self.food_id or self.bundle_id:
                raise ValueError("When type is 'supplier', only supplier_id must be set.")
        elif self.type == "bundle":
            if self.bundle_id is None or self.food_id or self.supplier_id:
                raise ValueError("When type is 'bundle', only bundle_id must be set.")
        return self

class FavoriteOut(BaseModel):
    target_id: int

class FavoriteListResponse(BaseModel):
    items: List[Union[FoodOut, SupplierOut, FoodBundleOut]]
