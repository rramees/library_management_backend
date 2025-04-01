from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.db.base import Base
import enum

class BorrowStatus(enum.Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"

class Borrowing(Base):
    __tablename__ = "borrowing"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    borrow_date = Column(DateTime, default=datetime.now, index=True)
    due_date = Column(DateTime, default=lambda: datetime.now() + timedelta(days=14), index=True)
    return_date = Column(DateTime, nullable=True)
    status = Column(Enum(BorrowStatus, values_callable=lambda obj: [e.value for e in obj]), default=BorrowStatus.BORROWED, index=True)

    user = relationship("User", backref="borrowings", lazy="joined")
    book = relationship("Book", backref="borrowings", lazy="joined")
    
    __table_args__ = (
        Index('idx_borrowing_status_due_date', status, due_date),
        Index('idx_borrowing_user_status', user_id, status),
    )
