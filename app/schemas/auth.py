from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    user_id: int
    email: EmailStr

class LoginResponse(BaseModel):
    access_token: str
    user: UserOut
