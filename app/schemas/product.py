from pydantic import BaseModel
from typing import List, Optional

class ProductRequest(BaseModel):
    type:str
    value:str

class ProductResponse(BaseModel):
    product_id:int
    name:str
    image_url:str
    allergen_hit:list[str]
    allergen_safe:list[str]
    ingredient:str
    is_favorite:bool
    supplier_id:int
    supplier_name:str

class BundleResponse(BaseModel):
    id:int
    name:str
    image_url:str
    supplier_id:int
    products:List[ProductResponse]

# 제품 등록
class ProductCreate(BaseModel):
    name: str
    ingredient: Optional[str] = None
    image_base64: Optional[str] = None  # 선택적
    allergies: List[str]  # 예: ["우유", "대두"]

class ProductCreateResponse(BaseModel):
    product_id: int
    name: str
    image_url: str
    ingredient: str
    supplier_id: int
    supplier_name: str