from pydantic import BaseModel

class AllergenGetResponse(BaseModel):
    allergies: list[str]

class AllergenSaveRequest(BaseModel):
    allergies: list[str]

class AllergenSaveResponse(BaseModel):
    message: str