from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    _id : str
    title: str
    isbn: str
    pageCount: int
    publishedDate: dict
    shortDescription: str
    longDescription: str
    status: Optional[str] = "meap"
    authors: list
    categories: list
    
    