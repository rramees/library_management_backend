from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.borrowing_repository import borrow_book, has_active_borrow
from app.db.models.user import User, UserRole
from app.db.models.book import Book

def process_borrowing(db: Session, user: User, book_id: int):
    if user.role != UserRole.USER:
        raise HTTPException(status_code=403, detail="Only normal users can borrow books")

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available_copies < 1:
        raise HTTPException(status_code=400, detail="Book is not available")

    if has_active_borrow(db, user.id, book_id):
        raise HTTPException(status_code=400, detail="You have already borrowed this book")

    borrowing = borrow_book(db, user, book)
    return borrowing
