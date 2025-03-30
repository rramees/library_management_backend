# from fastapi import Depends, HTTPException, status
# from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
# from jose import JWTError, jwt
# from sqlalchemy.orm import Session
# from app.db.models.user import User
# from app.db.session import get_db
# from app.core.config import settings

# # For JWT Authentication
# security_jwt = HTTPBearer()

# # For API Key Authentication
# api_key_header = APIKeyHeader(name='X-API-Key', auto_error=False)

# def verify_jwt_token(token: str, db: Session) -> User:
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         username = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token.")
#         user = db.query(User).filter(User.username == username).first()
#         if not user:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")
#         return user
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token.")

# def verify_api_key(api_key: str, db: Session) -> User:
#     user = db.query(User).filter(User.api_key == api_key).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key.")
#     return user

# # Unified Auth dependency
# async def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security_jwt),
#     api_key: str = Depends(api_key_header),
#     db: Session = Depends(get_db)
# ):
#     if credentials:
#         return verify_jwt_token(credentials.credentials, db)
#     elif api_key:
#         return verify_api_key(api_key, db)
#     else:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required.")


from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import secrets
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
