from fastapi import APIRouter, Depends, HTTPException, Request, status , Query
from app.db.models.user import User
from app.schemas.book_schema import BookCreate, BookResponse, BookUpdate
from app.services.book_service import add_book, get_filtered_books, process_book_update
from app.core.security import get_current_user, require_librarian
from app.db.session import get_db
from app.core.limiter import limiter 
from sqlalchemy.orm import Session
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
@limiter.limit("20/minute")
def search_books_api(
    request: Request,
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

@router.put("/{book_id}", response_model=BookResponse)
def update_book_by_id(
    book_id: int,
    updates: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian)
):
    updated = process_book_update(db, book_id, updates)
    return updated