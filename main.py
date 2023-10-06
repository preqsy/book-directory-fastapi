from fastapi import FastAPI, status, HTTPException
from model import Book

from database import database


def find(isbn):
    """returns the index of a dict"""
    for i, j in enumerate(database):
        if j["isbn"] == isbn:
            return i
        

app = FastAPI()


@app.get("/")
def home():
    return "Welcome"

@app.get("/books")
def all_posts():
    return database

@app.get("/books/{isbn}")
def single_post(isbn: str):   
    one_post = find(isbn)
    if one_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with isbn:{isbn} doesn't exist")
        
    single_post = database[one_post]
    
    return single_post


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book:Book):
    book_dict = book.dict()
    for j in database:
        if j["isbn"] == book_dict["isbn"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"book with isbn: {book_dict['isbn']} already exists")
    database.append(book_dict)
    return book_dict


@app.delete("/books/{isbn}", status_code=status.HTTP_202_ACCEPTED)
def remove_book(isbn):
    index = find(isbn)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with isbn{ isbn} doesn't exist")
    database.pop(index)
    return f"book successfully deleted"

@app.put("/books/{isbn}")
def update_book(isbn, book:Book):
    book_dict = book.dict()
    new_book = find(isbn)
    if new_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with isbn{ isbn} doesnt exists")
    book_dict["isbn"] = isbn
    
    database[new_book] = book_dict
    return "Book Updated"
