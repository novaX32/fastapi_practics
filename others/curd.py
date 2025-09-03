from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None
class Friends(BaseModel):
    name:str
    roll_no:int
    common_name:str
my_data=[{"id":1,"name":"Aarya","roll_no":28},{"id":2,"name":"Nikhil","roll_no":29},{"id":3,"name":"Mahesh","roll_no":30}]
chutiya_friends=[{"name":"Nikhil","roll_no":27,"common_name":"NovaX"}]

@app.get("/")
def root():
    return {"message": "Hello, I'm Optimus Prime"}

@app.get("/posts")
def get_data():
    return {"Data": my_data}

@app.post("/posts")
def create_post3(new_post: Post):
   new_post=new_post.model_dump()
   new_post["id"]=randrange(0,1000000)
   my_data.append(new_post)
   return {"new_data": new_post}

@app.post("/PostFriends")
def create_friends(friends:Friends):
    friends=friends.model_dump()
    friends["id"]=randrange(0,10000)
    chutiya_friends.append(friends)
    return{"new_data":friends}

@app.get("/PostFriends")
def get_friends():
    return {"friends":chutiya_friends}




