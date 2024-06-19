from typing import Optional

from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
# pydantic is a framework that allows data verification
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_date: int

    def __init__(self, id, title, author, description, rating, publish_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date


class BookRequest(BaseModel):
    id: Optional[int]=None     # it can be an int or type None
    # id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)    # greater than, less than
    publish_date: int = Field(gt=1999, lt=2031)

    class Config:
        json_schema_extra={
            # Setting up a new kind of the schema, to below type:
            'example': {
                'title': 'A new book',
                'author': 'codingwithroby',
                'description': 'A new description of a book',
                'rating': 5,
                'publish_date': 2000
            }
        }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithrobv', 'A very nice book!', 5, 2016),
    Book(2, 'Be Fast with FastAPI', 'codingwithrobv', 'A great Book!', 5, 2022),
    Book(3, 'Master Enpoints', 'codingwithrobv', 'An awesome Book!', 5, 2019),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2029),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2030),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2017),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int=Path(gt=0)):     # {book_id}, take in as book_id input of function, will be a path parameter, regulated greater than 0
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')


@app.get("books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int=Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def filter_publish(publish_date: int):
    books_to_return=[]
    for book in BOOKS:
        # print(book.publish_date)
        if book.publish_date == publish_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):     #  datatype Body()
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    book.id=1 if len(BOOKS)==0 else BOOKS[-1].id+1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')

# This request is not returning anything
@app.delete("books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_id(book_id: int):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')

