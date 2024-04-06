from enum import Enum
from datetime import datetime

from pydantic import BaseModel, model_validator


class BookBase(BaseModel):
    title: str
    author: str
    publication_year: int
    publisher: str

    class Config:
        orm_mode = True


class BookInstanceBase(BaseModel):
    book_id: int
    total_count: int
    available_count: int

    class Config:
        orm_mode = True


class MoveTypes(str, Enum):
    back = 'back'
    out = 'out'


class BookMoveBase(BaseModel):
    action: MoveTypes

    class Config:
        orm_mode = True


class CreateBook(BookBase):
    class Config:
        orm_mode = True


class BookExisted(BookBase):
    id: int

    class Config:
        orm_mode = True


class CreateBookInstance(BookInstanceBase):
    class Config:
        orm_mode = True


class BookMove(BookMoveBase):
    id: int
    book_id: int
    move_date: datetime

    class Config:
        orm_mode = True
