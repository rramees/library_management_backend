from sqlalchemy.orm import Session
from app.repositories.user_repository import create_user
from app.core.security import create_jwt_token
from app.schemas.user_schema import UserCreate

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
