from sqlalchemy.orm import Session
from app.db.models.book import Book
from app.db.models.category import Category
from app.schemas.book_schema import BookCreate, BookUpdate
from typing import List, Optional

def create_book(db: Session, book_data: BookCreate) -> Book:
    book = Book(**book_data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def search_books(
    db: Session,
    title: Optional[str] = None,
    publisher: Optional[str] = None,
    language: Optional[str] = None,
    category: Optional[str] = None,
    page_no: int = 1,
    page_size: int = 10
) -> List[Book]:
    query = db.query(Book)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if publisher:
        query = query.filter(Book.publisher.ilike(f"%{publisher}%"))
    if language:
        query = query.filter(Book.language.ilike(f"%{language}%"))
    if category:
        query = query.join(Category).filter(Category.name.ilike(f"%{category}%"))

    offset = (page_no - 1) * page_size
    total_items = query.count()

    return query.offset(offset).limit(page_size).all(), total_items

def update_book(db: Session, book_id: int, updates: BookUpdate) -> Optional[Book]:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return None

    data = updates.model_dump(exclude_unset=True)

    if "total_copies" in data:
        new_total = data["total_copies"]
        if book.available_copies > new_total:
            raise ValueError("available_copies cannot exceed total_copies")

    for key, value in data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book
