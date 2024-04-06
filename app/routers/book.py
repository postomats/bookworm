from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends
from fastapi import status, HTTPException

from sqlalchemy.orm import Session

from ..models.database import get_db
from ..models import Books as book_model
from ..models import schemas


router = APIRouter()


@router.get('/', response_model=List[schemas.BookExisted])
def book_list(start: int = 0, end: int = 50, db: Session = Depends(get_db)):
    books = db.query(book_model.Book).filter(book_model.Book.id > start).filter(book_model.Book.id < end).all()
    if not books:
        raise HTTPException(400, {'error': 'bad request'})
    books = [book.__dict__ for book in books]
    
    return books


@router.post('/create', response_model=schemas.BookExisted)
def create_book(new_book: schemas.CreateBook, total_count: int = 1, db: Session = Depends(get_db)):
    book = book_model.Book(**new_book.dict())
    db.add(book)
    db.commit()
    db.refresh(book)
    
    instanse = book_model.BookInstance(book_id=book.id)
    instanse.total_count, instanse.available_count = total_count, total_count 
    db.add(instanse)
    db.commit()
    return book


@router.get('/{id}', response_model=schemas.BookExisted)
def get_book(id: int, db: Session = Depends(get_db)):
    book = db.query(book_model.Book).filter(book_model.Book.id == id).first()
    if not book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {'error': 'not found'})
    
    return book


@router.get('/{id}/instance', response_model=schemas.CreateBookInstance)
def get_book_instance(id: int, db: Session = Depends(get_db)):
    book = db.query(book_model.BookInstance).filter(book_model.BookInstance.book_id == id).first()
    if not book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {'error': 'not found'})
    
    return book


@router.post('/{id}/move', response_model=schemas.BookMove)
def move_book(id, move_type: schemas.MoveTypes, db: Session = Depends(get_db)):
    book_instance = db.query(book_model.BookInstance).filter(book_model.BookInstance.book_id == id).first()
    if not book_instance:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {'error': 'not found'})
    
    if move_type.value == schemas.MoveTypes.back and \
        book_instance.available_count == book_instance.total_count:
            raise HTTPException(400, {'error': 'bad request'})
    
    if move_type.value == schemas.MoveTypes.out and \
        book_instance.available_count <= 0:
        raise HTTPException(400, {'error': 'bad request'})
    
    move = book_model.BookMove(book_id=id, move_date=datetime.now(), action=move_type)
    db.add(move)

    if move_type.value == schemas.MoveTypes.back:
        book_instance.available_count += 1
    else:
        book_instance.available_count -= 1
    
    db.commit()
    db.refresh(move)
    
    return move.__dict__

