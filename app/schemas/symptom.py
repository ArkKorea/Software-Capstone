from pydantic import BaseModel
from datetime import date
    
class SymptomByDateRequest(BaseModel):
    date: date

class SymptomByDateResponse(BaseModel):
    skin: int
    stomach: int
    breath: int
    headache: int
    fatigue: int

class SymptomSaveRequest(BaseModel):
    date: date
    skin: int
    stomach: int
    breath: int
    headache: int
    fatigue: int

class SymptomSaveResponse(BaseModel):
    message: str