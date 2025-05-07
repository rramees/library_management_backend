from fastapi import APIRouter
from app.api.endpoints import auth , books , borrow , query

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

api_router.include_router(books.router, prefix="/books", tags=["Books"])

api_router.include_router(borrow.router, prefix="", tags=["Borrow"])

api_router.include_router(query.router, prefix="/query", tags=["Query"])