from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.borrowing_service import process_borrowing, process_return
from app.core.security import get_current_user
from app.db.models.user import User

router = APIRouter()

@router.post("/borrow/{book_id}")
def borrow_book_api(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    borrowing = process_borrowing(db, current_user, book_id)
    return {
        "message": "Book borrowed successfully",
        "borrow_id": borrowing.id,
        "due_date": borrowing.due_date
    }

@router.post("/return/{book_id}")
def return_book_api(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    borrowing = process_return(db, current_user, book_id)
    return {
        "message": "Book returned successfully",
        "return_date": borrowing.return_date
    }

