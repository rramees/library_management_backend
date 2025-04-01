from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.book_schema import BookCreate
from app.services.book_service import add_book
from app.core.security import require_librarian
from app.db.session import get_db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_new_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_librarian)
):
    try:
        new_book = add_book(db, book)
        return {"message": "Book added successfully", "book_id": new_book.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding book: {str(e)}")
