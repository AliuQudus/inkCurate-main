
from pydoc import text
from sqlalchemy import TIMESTAMP, Column, Integer, text, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Login(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )