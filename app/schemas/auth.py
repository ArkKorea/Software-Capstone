from pydantic import BaseModel, EmailStr
from datetime import date

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    user_id: int
    email: EmailStr

class LoginResponse(BaseModel):
    access_token: str
    user: UserOut

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    birthdate: date
    agree_personal_info: bool

class RegisterResponse(BaseModel):
    message: str