from pydantic import BaseModel
from typing import List
from app.schemas.product import ProductResponse, BundleResponse

class SearchRequest(BaseModel):
    type: str
    query: str

class Store(BaseModel):
    store_id: int
    name: str
    address: str = None
    is_favorite: bool

class Bundle(BaseModel):
    bundle_id: int
    name: str
    image_url: str
    allergen_hit: List[str]
    allergen_safe: List[str]
    supplier_id: int
    supplier_name: str
    is_favorite: bool


class SearchStoreResponse(BaseModel):
    stores: List[Store]

class StoreProductListRequest(BaseModel):
    store_id: int

class StoreProductListResponse(BaseModel):
    store: Store
    products: List[ProductResponse]

class SearchProductResponse(BaseModel):
    products: List[ProductResponse]
    bundles: List[Bundle]