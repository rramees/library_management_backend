from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user_repository import create_user, get_user_by_username
from app.core.security import create_jwt_token, verify_password
from app.schemas.user_schema import UserCreate, UserLogin

def register_user(db: Session, user_create: UserCreate):
    user = create_user(
        db=db,
        username=user_create.username,
        password=user_create.password,
        email=user_create.email,
        full_name=user_create.full_name
    )
    
    jwt_token = create_jwt_token(user.username)
    
    return {
        "access_token": jwt_token,
        "api_key": user.api_key
    }

def login_user(db: Session, login_data: UserLogin):
    user = get_user_by_username(db, login_data.username)

    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token(user.username)
    return {
        "access_token": token,
        "api_key": user.api_key
    }