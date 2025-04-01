from sqlalchemy.orm import Session
from app.db.models.borrowing import Borrowing, BorrowStatus
from app.db.models.book import Book
from app.db.models.user import User
from datetime import datetime, timedelta

def borrow_book(db: Session, user: User, book: Book) -> Borrowing:
    borrowing = Borrowing(
        user_id=user.id,
        book_id=book.id,
        borrow_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=14),
        status=BorrowStatus.BORROWED
    )
    book.available_copies -= 1
    db.add(borrowing)
    db.commit()
    db.refresh(borrowing)
    return borrowing

def has_active_borrow(db: Session, user_id: int, book_id: int) -> bool:
    return db.query(Borrowing).filter(
        Borrowing.user_id == user_id,
        Borrowing.book_id == book_id,
        Borrowing.status == BorrowStatus.BORROWED
    ).first() is not None

def return_book(db: Session, user_id: int, book_id: int):
    from app.db.models.borrowing import BorrowStatus
    from datetime import datetime

    borrowing = db.query(Borrowing).filter(
        Borrowing.user_id == user_id,
        Borrowing.book_id == book_id,
        Borrowing.status == BorrowStatus.BORROWED
    ).first()

    if not borrowing:
        return None

    borrowing.status = BorrowStatus.RETURNED
    borrowing.return_date = datetime.utcnow()

    borrowing.book.available_copies += 1

    db.commit()
    db.refresh(borrowing)
    return borrowing

