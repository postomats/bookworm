from .database import Base, engine

from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, DateTime, Enum
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    publication_year = Column(Integer)
    publisher = Column(String)

    instances = relationship("BookInstance", back_populates="book")
    moves = relationship("BookMove", back_populates="book")


class BookInstance(Base):
    __tablename__ = 'book_instances'

    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    total_count = Column(Integer)
    available_count = Column(Integer)

    book = relationship("Book", back_populates="instances")


class BookMove(Base):
    __tablename__ = 'book_move'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    move_date = Column(DateTime)

    # Возможные значения: 'возврат', 'выдача'
    action = Column(Enum('out', 'back', name="pgenum"))

    book = relationship("Book", back_populates="moves")


Base.metadata.create_all(bind=engine)
