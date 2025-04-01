from sqlalchemy.orm import Session
from app.db.models.user import User
from typing import Optional
from app.core.security import hash_password, generate_api_key
from app.schemas.user_schema import UserResponse

def create_user(db: Session, username: str, password: str, email: str, full_name: str):
    hashed_pw = hash_password(password)
    api_key = generate_api_key()
    
    user = User(
        username=username,
        password=hashed_pw,
        email=email,
        full_name=full_name,
        api_key=api_key
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


def get_user_by_username(db: Session, username: str) -> Optional[UserResponse]:
    return db.query(User).filter(User.username == username).first()
