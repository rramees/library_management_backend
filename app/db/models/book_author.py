from sqlalchemy import Column, Integer, ForeignKey, Index
from app.db.base import Base

class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)
    
    __table_args__ = (
        Index('idx_book_author', book_id, author_id),
    )
