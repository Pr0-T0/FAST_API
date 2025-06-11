from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from  sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal() #Creates a new Session
        yield db            # Yield the session to the path operation
    finally:
        db.close()          # Ensure the session is closed after the request


                            # When you use Depends(get_db) in a route handler, FastAPI:

                            # Calls get_db(), which creates a session.

                            # Passes the db session to your route function.

                            # Once the function completes (even if it fails), finally is triggered to close the session.


class Book(BaseModel): #validation class
    title:str = Field(min_length = 1)
    author: str = Field(min_length = 1, max_length = 100)
    description:str = Field(min_length = 1, max_length = 100)
    rating:int = Field(gt=-1, lt=101)

# BOOKS = []

@app.get("/") #path parameter
def read_api(db:Session = Depends(get_db)):
    return db.query(models.Books).all()  #return all table contents

@app.post("/")
def create_book(book : Book, db:Session = Depends(get_db)): #parameter for dependency injection
    
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book

@app.put("/{book_id}")
def update_book(book_id: int, book:Book, db:Session = Depends(get_db)):
    
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first() #update query where books.id = book_id 

    if book_model is None: #guard clause or exception
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id}: Does not exist"
        )

    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)

    db.commit()

    return book

@app.delete("/{book_id}")
def delete_book(book_id:int, db:Session = Depends(get_db)):
    
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} does not exist"
        )
    db.query(models.Books).filter(models.Books.id == book_id).delete()

    db.commit()