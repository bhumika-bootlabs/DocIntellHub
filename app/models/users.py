from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    # username: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserSignup(BaseModel):
    # username: str
    email: EmailStr
    password: str
    role: str
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app.models.base import Base   
# Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")



