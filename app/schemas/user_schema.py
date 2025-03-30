from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str
    phone_no: str = None
    status: str = "active"

class UserCreate(UserBase):
    pass

class RegisterResponse(BaseModel):
    access_token: str
    api_key: str
