from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

    
class CreatePost(PostBase):
  pass


# Request model for creating an user

class CreateUser(BaseModel):
  email: EmailStr
  password: str
  
  class Config:
    orm_mode = True


class UserLogin(BaseModel):
  email: EmailStr
  password: str
  
  class Config:
    orm_mode = True

# Response model after creating an user

class UserResponse(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime
  
  # to work sqlalchemy with pydantic (docs) 
  class Config:
    orm_mode = True

# Response should contain following fields

class ResponseModel(PostBase):
  id: int
  created_at: datetime
  userId: int
  user: UserResponse
  
  # to work sqlalchemy with pydantic (docs) 
  class Config:
    orm_mode = True

#  While adding like in the response followin shcema should be the response model instead of class ResponseModel

class ResponseModelWithLike(BaseModel):
  Post: ResponseModel
  likes: int
  
  class Config:
    orm_mode = True


class Token(BaseModel):
  access_token: str
  token_type: str
  
  class Config:
    orm_mode = True
  
  
class TokenData(BaseModel):
  id: Optional[str] = None
  
  class Config:
    orm_mode = True


class Like(BaseModel):
  postId: int
  direction: conint(le=1)
  
  class Config:
    orm_mode = True

