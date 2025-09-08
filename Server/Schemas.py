from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
  Name: str
  username: str
  email: EmailStr
  password: str

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
