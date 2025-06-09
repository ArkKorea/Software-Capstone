from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class SourceType(str, Enum):
    user = "user"
    ocr = "ocr"
    crowl = "crowl"

class FoodOut(BaseModel):
    id: int
    name: str
    ingredient: str | None
    image_url: str | None
    source_type: SourceType
    supplier_id: int
    created_at: datetime

    class Config:
        from_attributes = True
