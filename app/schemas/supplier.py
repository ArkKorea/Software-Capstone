from pydantic import BaseModel
from datetime import datetime
from app.schemas.product import ProductResponse

from typing import Optional, List

class SupplierOut(BaseModel):
    id: int
    name: str
    contact_email: str | None
    business_license_number: str | None
    is_verified: bool
    image_url: str | None
    created_at: datetime

    class Config:
        from_attributes = True

# SupplierDetailResponse에서 사용하기 위한 bundle response의 축약형
class BundleSummary(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None
    is_favorite: bool

class SupplierDetailResponse(BaseModel):
    id: int
    name: str
    image_url: Optional[str]
    products: List[ProductResponse]
    bundles: List[BundleSummary]  # 이름, id, 이미지만
    is_favorite: bool
    address: str | None = None
