'''
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List


class User(BaseModel):
    Name: str
    username: str
    email: EmailStr
    password: str


class UpdateUser(BaseModel):
    Name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


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
    
    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class VoteUser(BaseModel):
    username: str
    name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class BookVoteResponse(BaseModel):
    google_book_id: str
    title: Optional[str] = None
    thumbnail: Optional[str] = None
    vote_count: int
    users: List[VoteUser] = []
    
    model_config = ConfigDict(from_attributes=True)


class BookVoteAction(BaseModel):
    google_book_id: str
    title: Optional[str] = None
    authors: Optional[str] = None
    thumbnail: Optional[str] = None
    action: Optional[str] = "like"  # "like" or "unlike"


# Additional schemas for Google Books integration
class GoogleBookSummary(BaseModel):
    google_book_id: str
    title: Optional[str] = None
    authors: List[str] = []
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    publishedDate: Optional[str] = None
    is_liked: bool = False
    vote_count: int = 0


class GoogleBookDetail(GoogleBookSummary):
    """Extended detail view for a single book"""
    pass
    '''

from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List
from uuid import UUID


class User(BaseModel):
    Name: str
    username: str
    email: EmailStr
    Phone_No: Optional[str] = None
    password: str


class UpdateUser(BaseModel):
    Name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class UpdateOutput(BaseModel):
    id:UUID
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
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    id: Optional[UUID] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class VoteUser(BaseModel):
    username: str
    name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class BookVoteResponse(BaseModel):
    google_book_id: str
    title: Optional[str] = None
    thumbnail: Optional[str] = None
    vote_count: int
    users: List[VoteUser] = []
    
    model_config = ConfigDict(from_attributes=True)


class BookVoteAction(BaseModel):
    google_book_id: str
    title: Optional[str] = None
    authors: Optional[List[str]] = None  # Changed to list
    thumbnail: Optional[str] = None
    description: Optional[str] = None
    published_date: Optional[str] = None
    action: Optional[str] = "like"  # "like" or "unlike"


# Additional schemas for Google Books integration
class GoogleBookSummary(BaseModel):
    google_book_id: str
    title: Optional[str] = None
    authors: List[str] = []
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    publishedDate: Optional[str] = None
    is_liked: bool = False
    vote_count: int = 0


class GoogleBookDetail(GoogleBookSummary):
    """Extended detail view for a single book"""
    pass