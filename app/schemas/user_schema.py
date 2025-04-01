from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str
    phone_no: str
    role: str
    status: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class RegisterResponse(BaseModel):
    access_token: str
    api_key: str
