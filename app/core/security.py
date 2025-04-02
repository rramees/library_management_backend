from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.db.models.user import User, UserRole, UserStatus
from app.db.session import get_db
from passlib.context import CryptContext
from datetime import datetime, timedelta
import secrets


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

bearer_scheme = HTTPBearer(auto_error=False)
api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def generate_api_key():
    return secrets.token_urlsafe(32)

def create_jwt_token(username: str, expires_delta: timedelta = timedelta(hours=24)):
    expire = datetime.now() + expires_delta
    to_encode = {"exp": expire, "sub": username}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_jwt(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    api_key: str = Depends(api_key_scheme),
    db: Session = Depends(get_db)
) -> User:
    user = None

    if token:
        username = decode_jwt(token.credentials)
        if username:
            user = db.query(User).filter(User.username == username).first()
    elif api_key:
        user = db.query(User).filter(User.api_key == api_key).first()

    if not user or user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or inactive user"
        )

    return user

def require_librarian(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.LIBRARIAN:
        raise HTTPException(status_code=403, detail="Librarian access required")
    return user
