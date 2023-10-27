from fastapi import FastAPI, status, HTTPException
from dotenv import find_dotenv, load_dotenv
from model import Book
import os
from pymongo import MongoClient

load_dotenv(find_dotenv())
password = os.environ.get("MONGO_PWD")
MONGO_URI = f"mongodb+srv://Preqsy:{password}@cluster0.xvggsoe.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(MONGO_URI)

db = cluster["books"]
col = db["books"]
        
app = FastAPI()


@app.get("/")
def home():
    return "Welcome"

@app.get("/books", status_code=status.HTTP_202_ACCEPTED)
def all_posts():
    results = col.find()
    
    books_list = [x for x in results]
    if books_list  == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books found")

    return books_list

@app.get("/books/{isbn}", status_code=status.HTTP_202_ACCEPTED)
def single_post(isbn: str):
    books = {
        "isbn": isbn
    }
    book = col.find_one(books)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with isbn: {isbn} do not exist")   
    
    
    return book


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book:Book):
    book_dict = book.dict()
    book_dict["_id"] =  book_dict["isbn"]
    if col.find_one({"_id" : book_dict["_id"]}) == None:
        col.insert_one(book_dict)
        return f"""Book with title "{book_dict['title']}" has been created"""
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Book with isbn: {book_dict['_id']} already exists")


@app.delete("/books/{isbn}", status_code=status.HTTP_204_NO_CONTENT)
def remove_book(isbn):
    book_dict = {
        "isbn" : isbn
    }
    find_book = col.find_one(book_dict)
    if find_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with isbn: {isbn} doesn't exist")
    book = col.delete_one(book_dict)
    return f"book successfully deleted"

@app.put("/books/{isbn}", status_code=status.HTTP_202_ACCEPTED)
def update_book(isbn, book:Book):
    book_dict = book.dict()
    isbn_check = col.find_one({"isbn": isbn})
    if isbn_check == None:
        print(f"*************{isbn_check}***************")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with isbn:{isbn} doesn't exists") 
    elif isbn is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Pass in an ISBN")
    print(f"*************{isbn_check}***************")
    col.replace_one({"isbn": isbn}, book_dict)
    return "Book Updated"
