'''
from sqlalchemy import TIMESTAMP, Column, Integer, String, text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class Login(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    # relationship backrefs
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    google_book_id = Column(String, nullable=False, unique=True, index=True)
    title = Column(String, nullable=True)
    authors = Column(String, nullable=True)  # store comma-separated string
    thumbnail = Column(String, nullable=True)
    description = Column(String, nullable=True)  # Optional: store book description
    published_date = Column(String, nullable=True)  # Optional: store publication date
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()"))

    likes = relationship("Like", back_populates="book", cascade="all, delete-orphan")


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    user = relationship("Login", back_populates="likes")
    book = relationship("Book", back_populates="likes")

    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="uq_user_book"),
    )
    '''

from sqlalchemy import TIMESTAMP, Column, Integer, String, text, ForeignKey, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from .database import Base

class Login(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    # relationship backrefs
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    google_book_id = Column(String, nullable=False, unique=True, index=True)
    title = Column(String, nullable=True)
    authors = Column(JSON, nullable=True)  # store as JSON array
    thumbnail = Column(String, nullable=True)
    description = Column(String, nullable=True)  # Optional: store book description
    published_date = Column(String, nullable=True)  # Optional: store publication date
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()"))

    likes = relationship("Like", back_populates="book", cascade="all, delete-orphan")


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    user = relationship("Login", back_populates="likes")
    book = relationship("Book", back_populates="likes")

    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="uq_user_book"),
    )