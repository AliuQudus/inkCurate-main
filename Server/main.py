from fastapi import FastAPI
#from routers import google_books
from . import models
from .database import engine
from .routers import user, auth, google_books, book
from fastapi.middleware.cors import CORSMiddleware
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"] # To allow all website to access your api
# origins = ["https://www.google.com"] # To allow a specigic website to access your api

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(google_books.router)



@app.get("/")
async def root():
    return {"message": "Hello World"}