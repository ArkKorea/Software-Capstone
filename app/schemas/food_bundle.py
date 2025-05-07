from pydantic import BaseModel
from datetime import datetime

class FoodBundleOut(BaseModel):
    id: int
    name: str
    image_url: str | None
    supplier_id: int
    created_at: datetime

    class Config:
        from_attributes = True
