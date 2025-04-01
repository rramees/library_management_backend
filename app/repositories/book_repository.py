from sqlalchemy.orm import Session
from app.db.models.book import Book
from app.schemas.book_schema import BookCreate

def create_book(db: Session, book_data: BookCreate) -> Book:
    book = Book(**book_data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
