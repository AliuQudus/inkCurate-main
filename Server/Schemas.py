from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class User(BaseModel):
  Name: str
  username: str
  email: EmailStr
  password: str
class UpdateUser(BaseModel):
  Name: Optional[str] = None
  username: Optional[str] = None
  password: Optional[str] = None

  model_config = {"from_attributes": True}

class UpdateOutput(BaseModel):
  Name: str
  username: str
  email: EmailStr

class UserOutput(BaseModel):
  Name: str
  email: EmailStr
  created_at: datetime


class UserLogin(BaseModel):
  email: str
  password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None