from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.security import hash_password, generate_api_key

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
