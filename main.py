from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str

books: List[Book] = []

@app.get("/books", response_model=List[Book])
def get_books():
    return books

@app.post("/books", response_model=Book)
def add_book(book: Book):
    # Verifica se o ID já existe
    for b in books:
        if b.id == book.id:
            raise HTTPException(status_code=400, detail="O ID desse Livro já existe.")
    books.append(book)
    return book

@app.get("/books/{book_id}", response_model=Book)
def get_book_by_id(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Livro não encontrado.")
