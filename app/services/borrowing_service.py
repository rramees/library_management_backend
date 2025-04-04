from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.borrowing_repository import borrow_book, get_user_borrow_history, has_active_borrow, return_book
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

def process_return(db: Session, user: User, book_id: int):
    if user.role != UserRole.USER:
        raise HTTPException(status_code=403, detail="Only users can return books")

    borrowing = return_book(db, user.id, book_id)
    if not borrowing:
        raise HTTPException(status_code=404, detail="No active borrow record for this book")

    return borrowing

def fetch_borrow_history(db: Session, user_id: int):
    return get_user_borrow_history(db, user_id)
