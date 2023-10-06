from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    title: str
    isbn: str
    pageCount: int
    publishedDate: dict
    shortDescription: str
    longDescription: str
    status: Optional[str] = "meap"
    authors: list
    categories: list
    