from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class ViewLogItem(BaseModel):
    type: Literal["food", "bundle", "supplier"]
    id: int  # 실제 대상의 ID (food_id, bundle_id, supplier_id 중 하나)
    name: str
    image_url: Optional[str] = None
    viewed_at: datetime

class ViewLogResponse(BaseModel):
    products: list[ViewLogItem]
