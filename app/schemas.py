from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional
# from pydantic.types import conint

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

class PostCreate(PostBase):
    pass
class UserCreate(BaseModel):
   email:EmailStr
   password:str

class UserOut(BaseModel):
   id:int
   email:EmailStr
   created_at:datetime
   class Config:
      from_attributes=True

class UserLogin(BaseModel):
   email:EmailStr
   password:str
   
class Token(BaseModel):
   access_token:str
   token_type:str

class TokenData(BaseModel):
   id:Optional[int]=None

class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserOut
    class Config:
     from_attributes=True
     
class PostOut(PostBase):
    id: int
    
    owner_id: int
    votes: int

    class Config:
        orm_mode = True

class Vote(BaseModel):
   post_id:int
   dir:int=Field(...,le=1,ge=0)




   




   

