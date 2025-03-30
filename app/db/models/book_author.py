from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base

class BookAuthor(Base):
    __tablename__ = "book_authors"

    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)
