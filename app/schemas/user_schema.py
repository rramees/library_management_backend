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
