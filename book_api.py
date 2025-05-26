from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from prometheus_client import Counter, Histogram, Gauge
import time

router = APIRouter()

# Modelo de dados para um livro
BOOKS_COUNTER = Counter('books_total', 'Número total de livors no sistema')
REQUESTS_COUNTER = Counter('http_requests_total', 'Total de requisições por rota', ['method', 'endpoint', 'status'])
RESPONSE_TIME = Histogram('http_request_duration_seconds', 'Tempo de resposta por rota',
                         ['method', 'endpoint'],
                         buckets=[0.1, 0.5, 1.0, 2.0, 5.0])

ERROR_COUNTER = Counter('http_errors_total', 'Total de erros por rota', ['method', 'endpoint', 'error_type'])
BOOKS_GAUGE = Gauge('current_books', 'Current number of books in the system')

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

def instrument_request(method: str, endpoint: str):
    start_time = time.time()
    def callback(status_code: int, error_type: str = None):
        duration = time.time() - start_time
        REQUESTS_COUNTER.labels(method=method, endpoint=endpoint, status=status_code).inc()
        RESPONSE_TIME.labels(method=method, endpoint=endpoint).observe(duration)
        if error_type:
            ERROR_COUNTER.labels(method=method, endpoint=endpoint, error_type=error_type).inc()
    return callback

# Rotas
@router.get("/books", response_model=List[Book])
def list_books():
    callback = instrument_request('GET', '/books')
    try:
        result = books
        callback(200)
        return result
    except Exception as e:
        callback(500, str(type(e).__name__))
        raise

@router.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    callback = instrument_request('GET', '/books/{book_id}')
    try:
        book = find_book_by_id(book_id)
        if book is None:
            callback(404, 'NotFoundError')
            raise HTTPException(status_code=404, detail="Livro não encontrado.")
        callback(200)
        return book
    except HTTPException as e:
        callback(e.status_code, 'HTTPException')
        raise
    except Exception as e:
        callback(500, str(type(e).__name__))
        raise

@router.post("/books", response_model=Book, status_code=201)
def create_book(book: Book):
    callback = instrument_request('POST', '/books')
    try:
        if book_id_exists(book.id):
            callback(400, 'DuplicateIDError')
            raise HTTPException(status_code=400, detail="O ID desse livro já existe.")
        books.append(book)
        BOOKS_COUNTER.inc()
        BOOKS_GAUGE.set(len(books))
        callback(201)
        return book
    except HTTPException as e:
        callback(e.status_code, 'HTTPException')
        raise
    except Exception as e:
        callback(500, str(type(e).__name__))
        raise
