from pydantic import BaseModel
from typing import Optional, Literal, Union, List
from datetime import datetime
from app.schemas.product import ProductResponse
from app.schemas.search import Store, Bundle
from app.schemas.supplier import SupplierDetailResponse

class ViewLogItem(BaseModel):
    type: Literal["food", "bundle", "supplier"]
    id: int  # 실제 대상의 ID (food_id, bundle_id, supplier_id 중 하나)
    name: str
    image_url: Optional[str] = None
    viewed_at: datetime

class ViewLogResponse(BaseModel):
    products: list[ViewLogItem]

class HistoryItem(BaseModel):
    type: Literal["food", "bundle", "supplier"]
    viewed_at: datetime
    data: Union[ProductResponse, Bundle, SupplierDetailResponse]

class UnifiedHistoryResponse(BaseModel):
    history: List[HistoryItem]

class HistoryLogRequest(BaseModel):
    type: Literal["food", "bundle", "supplier"]
    target_id: int