from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user_schema import UserCreate, RegisterResponse
from app.services.auth_service import register_user

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    try:
        result = register_user(db, user_create)
        return {
            "access_token": result["access_token"],
            "api_key": result["api_key"]
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
