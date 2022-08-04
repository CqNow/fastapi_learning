from fastapi import FastAPI, Query, Path, Body
from schemas import Author, Book
from typing import List

app = FastAPI()


@app.post('/book')
def create_book(item: Book, author: Author, quantity: int = Body(...)):
    return {"item" : item, "author" : author, 'quantity' : quantity}

@app.post('/author')
def create_author(author: Author = Body(..., embed=True)):
    return {"author" : author}


@app.get('/book')
def get_book(q: List[str] = Query(['test1', 'test2'], description='Search Book', deprecated=True)):
    return q


@app.get('/book/{pk}')
def get_single_book(pk: int = Path(..., gt=1, le=20), pages: int = Query(None, gt=10, le=500)):
    return {'pk' : pk, 'pages' : pages}








