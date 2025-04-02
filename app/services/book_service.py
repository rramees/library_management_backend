from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Dict
from app.schemas.book_schema import BookCreate, BookUpdate
from app.repositories.book_repository import create_book, search_books, update_book

def add_book(db: Session, book_data: BookCreate):
    return create_book(db, book_data)

def get_filtered_books(
    db: Session,
    title: Optional[str] = None,
    publisher: Optional[str] = None,
    language: Optional[str] = None,
    category: Optional[str] = None,
    page_no: int = 1,
    page_size: int = 10
) -> Dict:
    books, total_items = search_books(
        db,
        title=title,
        publisher=publisher,
        language=language,
        category=category,
        page_no=page_no,
        page_size=page_size
    )

    total_pages = (total_items + page_size - 1) // page_size

    return {
        "books": books,
        "pagination": {
            "page_no": page_no,
            "page_size": page_size,
            "total_pages": total_pages,
            "total_items": total_items
        }
    }

def process_book_update(db: Session, book_id: int, updates: BookUpdate):
    try:
        updated = update_book(db, book_id, updates)
        if not updated:
            raise HTTPException(status_code=404, detail="Book not found")
        return updated
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))