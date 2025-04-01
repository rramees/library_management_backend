from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    publisher: str
    category_id: int
    total_copies: int
    available_copies: int
    language: str

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True

class BookUpdate(BaseModel):
    title: Optional[str]
    publisher: Optional[str]
    category_id: Optional[int]
    total_copies: Optional[int]
    available_copies: Optional[int]
    language: Optional[str]