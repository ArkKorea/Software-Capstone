from pydantic import BaseModel
from typing import List, Text, Optional
from datetime import datetime, date

class SuggestedProduct(BaseModel):
    product_id : int
    name: str
    image_url: str
    match_score: float

class MatchedProduct(BaseModel):
    product_id: int
    name: str
    image_url: Optional[str] = None
    supplier_id: int
    supplier_name: str

class CreateMealRequest(BaseModel):
    datetime: datetime
    food_name: str
    quantity: int
    memo: Text

class CreateMealResponse(BaseModel):
    record_id: int
    suggested_products: List[SuggestedProduct]


class ConnectMealRequest(BaseModel):
    record_id: int
    matched_product_id: int
    
class ConnectMealResponse(BaseModel):
    message: str

class Meal(BaseModel):
    datetime: datetime
    food_name: str
    matched_product: Optional[MatchedProduct] = None
    quantity: int
    memo: Text

class QueryMealRequest(BaseModel):
    date: date
    
class QueryMealResponse(BaseModel):
    meals: List[Meal]