import Schemas
from fastapi import Depends, APIRouter, Body, HTTPException, status, Path
from sqlalchemy.orm import Session

from . import Schemas, models
from ..database import get_db

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login (user_details: Schemas.UserLogin, db: Session = Depends(get_db)):

  user = (db.query(models.Login).filter(models.Login.email == user_details.email).first())

  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")