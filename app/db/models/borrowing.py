from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
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
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=14))
    return_date = Column(DateTime, nullable=True)
    status = Column(Enum(BorrowStatus), default=BorrowStatus.BORROWED)

    user = relationship("User", backref="borrowings")
    book = relationship("Book", backref="borrowings")
