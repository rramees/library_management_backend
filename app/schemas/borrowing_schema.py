from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.book_schema import BookResponse
from app.db.models.borrowing import BorrowStatus
from app.schemas.user_schema import UserPublic

class BorrowingHistoryResponse(BaseModel):
    id: int
    book: BookResponse
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    status: BorrowStatus
    user: UserPublic

    class Config:
        from_attributes = True
