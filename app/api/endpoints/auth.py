from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user_schema import UserCreate, RegisterResponse, UserLogin
from app.services.auth_service import login_user, register_user
from app.core.limiter import limiter 

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
@limiter.limit("10/minute")
def register(request: Request,user_create: UserCreate, db: Session = Depends(get_db)):
    try:
        result = register_user(db, user_create)
        return {
            "access_token": result["access_token"],
            "api_key": result["api_key"]
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=RegisterResponse)
@limiter.limit("10/minute")
def login(request: Request,login_data: UserLogin, db: Session = Depends(get_db)):
    try:
        result = login_user(db, login_data)
        print(f"Login result: {result}")
        return RegisterResponse(
            access_token=result["access_token"],
            api_key=result["api_key"]
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error during login")