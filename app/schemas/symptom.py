from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Text

class MatchedProduct(BaseModel):
    product_id: int
    name: str
    image_url: str
    supplier_id: int
    supplier_name: str  

class Meal(BaseModel):
    datetime: datetime
    food_name: str
    matched_prodeuct: MatchedProduct
    memo: Text
    
class SymptomByDateRequest(BaseModel):
    date: date

class SymptomByDateResponse(BaseModel):
    meals: List[Meal]

class SymptomSaveRequest(BaseModel):
    date: date
    skin: int
    stomach: int
    breath: int
    headache: int
    fatigue: int

class SymptomSaveResponse(BaseModel):
    message: str