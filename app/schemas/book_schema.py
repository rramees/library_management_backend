from pydantic import BaseModel

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
