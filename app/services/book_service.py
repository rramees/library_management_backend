from sqlalchemy.orm import Session
from app.schemas.book_schema import BookCreate
from app.repositories.book_repository import create_book

def add_book(db: Session, book_data: BookCreate):
    return create_book(db, book_data)
