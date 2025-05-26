from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from prometheus_client import Counter

router = APIRouter()

# Modelo de dados para um livro
BOOKS_COUNTER = Counter('books_total', 'Número total de livors no sistema')
BOOKS_REQUESTS_COUNTER = Counter('books_requests_total', 'Número total de requisições para livros', ['endpoint'])


class Book(BaseModel):
    id: int
    title: str
    author: str

# Array para armazenar os livros
books: List[Book] = []

# Funções auxiliares
def find_book_by_id(book_id: int) -> Book | None:
    return next((book for book in books if book.id == book_id), None)

def book_id_exists(book_id: int) -> bool:
    return any(book.id == book_id for book in books)

# Rotas
@router.get("/books", response_model=List[Book])
def list_books():
    BOOKS_REQUESTS_COUNTER.labels(endpoint='/books').inc()
    return books

@router.get("/health", response_model=dict)
def health_check():
    return {"status": "ok"}

@router.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    BOOKS_REQUESTS_COUNTER.labels(endpoint='/books/{book_id}').inc()
    book = find_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    return book

@router.post("/books", response_model=Book, status_code=201)
def create_book(book: Book):
    if book_id_exists(book.id):
        raise HTTPException(status_code=400, detail="O ID desse livro já existe.")
    books.append(book)
    BOOKS_COUNTER.inc()
    return book
