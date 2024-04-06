from .routers import book

from fastapi import FastAPI
from fastapi import status


app = FastAPI(title='bookworm API')
app.include_router(book.router, prefix='/book')

@app.get('/healcheck', status_code=status.HTTP_200_OK)
def index():
    return 'OK'