# placeholder
from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    # username: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    # username: str
    email: str
    role: str

    class Config:
        orm_mode = True