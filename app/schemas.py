from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.database import Base
from app.models import User
# To validate the 



class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True # Default value
    #rating: Optional[int] = None 

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    premium: bool
    created_at: datetime

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    premium: bool = False


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None