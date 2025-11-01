from fastapi import FastAPI
#from routers import google_books
from . import models
from .database import engine
from .routers import user, auth, google_books, book

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(google_books.router)



@app.get("/")
async def root():
    return {"message": "Hello World"}