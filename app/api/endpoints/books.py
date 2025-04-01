from fastapi import APIRouter, Depends, HTTPException, status , Query
from sqlalchemy.orm import Session
from app.schemas.book_schema import BookCreate
from app.services.book_service import add_book, get_filtered_books
from app.core.security import get_current_user, require_librarian
from app.db.session import get_db
from typing import Optional

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

@router.get("/search")
def search_books_api(
    title: Optional[str] = Query(None),
    publisher: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    page_no: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = get_filtered_books(
        db=db,
        title=title,
        publisher=publisher,
        language=language,
        category_id=category_id,
        page_no=page_no,
        page_size=page_size
    )

    return result