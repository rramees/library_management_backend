from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    publisher = Column(String(255))
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)
    language = Column(String(50), index=True)

    category = relationship("Category", backref="books", lazy="joined")
    authors = relationship("Author", secondary="book_authors", back_populates="books", lazy="selectin")
    
    __table_args__ = (
        Index('idx_book_title_language', title, language),
        Index('idx_book_availability', available_copies),
    )
