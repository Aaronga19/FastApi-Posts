from datetime import datetime
from pydantic import BaseModel, EmailStr
# To validate the 



class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True # Default value
    #rating: Optional[int] = None 

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
