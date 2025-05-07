from pydantic import BaseModel
from datetime import datetime

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
