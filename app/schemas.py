from pydantic import BaseModel, EmailStr
from datetime import datetime




class UserCreate(BaseModel):
    password: str
    email: EmailStr
    name: str

class UserResponse(BaseModel):
    created_at: datetime
    email: EmailStr
    name: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_id: int = None




class PostBase(BaseModel):
    title: str
    content: str
    visibility: str = "public"


# Creating a schema (base model) for posts using pydantic
class Post(PostBase):
    pass


class PostResponse(PostBase):
    created_at: datetime
    user_id: int


    class Config:
        orm_mode = True

