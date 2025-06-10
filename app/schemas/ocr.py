from typing import List, Optional
from pydantic import BaseModel
from app.schemas.meal import SuggestedProduct

class OCRProductResponse(BaseModel):
    product_id: int
    name: str
    image_url: Optional[str]
    allergen_hit: List[str]
    allergen_safe: List[str]
    ingredient: str
    supplier_id: int
    created_at: Optional[str]
    suggested_products: List[SuggestedProduct]
