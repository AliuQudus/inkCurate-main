from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models
from .database import engine, get_db
from .routers import user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}