from pydantic import BaseModel
from typing import List

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