from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.borrowing_schema import BorrowingHistoryResponse
from app.services.borrowing_service import fetch_borrow_history, process_borrowing, process_return
from app.core.security import get_current_user
from app.db.models.user import User, UserRole

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

@router.get("/history/me", response_model=List[BorrowingHistoryResponse])
def get_my_borrowing_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return fetch_borrow_history(db, current_user.id)

@router.get("/history/{user_id}", response_model=List[BorrowingHistoryResponse])
def get_user_borrowing_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.LIBRARIAN:
        raise HTTPException(status_code=403, detail="Only librarians can access other users' history")

    return fetch_borrow_history(db, user_id)
