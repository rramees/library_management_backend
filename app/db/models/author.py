from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from app.db import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    nationality = Column(String(100), index=True)

    books = relationship("Book", secondary="book_authors", back_populates="authors", lazy="selectin")
    
    __table_args__ = (
        Index('idx_author_name_nationality', name, nationality),
    )
