from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class FoodBundleOut(BaseModel):
    id: int
    name: str
    image_url: str | None
    supplier_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# 번들 생성
class BundleCreate(BaseModel):
    name: str
    image_base64: Optional[str] = None
    product_ids: List[int]

# 번들 조회
class BundleListItem(BaseModel):
    id: int
    name: str
    image_url: Optional[str]

class BundleListResponse(BaseModel):
    bundles: List[BundleListItem]

# 번들 수정
class BundleUpdate(BaseModel):
    bundle_id: int
    name: Optional[str] = None
    image_base64: Optional[str] = None
    product_ids: Optional[List[int]] = None  # 교체

# 번들 삭제
class BundleDelete(BaseModel):
    bundle_id: int