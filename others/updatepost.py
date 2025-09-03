from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None



class Friend(BaseModel):
    name: str
    roll_no: int
    common_name: str

my_data = [{"id": 1, "name": "Aarya", "roll_no": 28},
           {"id": 2, "name": "Nikhil", "roll_no": 29},
           {"id": 3, "name": "Mahesh", "roll_no": 30}]

my_friends = [{"name": "Nikhil", "roll_no": 27, "common_name": "NovaX"}]

@app.get("/")
def root():
    return {"message": "Hello, I'm Optimus Prime"}

@app.get("/posts")
def get_data():
    return {"Data": my_data}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    new_post = new_post.model_dump()
    new_post["id"] = randrange(0, 1000000)
    my_data.append(new_post)
    return {"new_data": new_post}

@app.post("/postfriends")
def create_friend(friend: Friend):
    friend = friend.model_dump()
    friend["id"] = randrange(0, 10000)
    my_friends.append(friend)
    return {"new_data": friend}

@app.get("/postfriends")
def get_friends():
    return {"friends": my_friends}

@app.get("/posts/latest")
def get_latest():
    post = my_data[-1]
    return {"data": post}

def find_post(id: int):
    for p in my_data:
        if p["id"] == id:
            return p
    return None



@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Bro {id} is not found")
    return {"data": post}


# <--------------DELETE POST-------------------->

def find_index_post(id: int):
    for index, post in enumerate(my_data):
        if post["id"] == id:
            return index
    return None



# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     index = find_index_post(id)
#     if index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id {id} does not exist")
#     my_data.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.delete("/posts/{id}")
# def delete_post(id: int):
#     index = find_index_post(id)
#     if index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id {id} does not exist")
#     my_data.pop(index)
#     return {"message": "Post deleted successfully"}

# <------------------------------UPDATE POST------------------------------------------------------>
# @app.put("/posts/{id}", status_code=status.HTTP_200_OK)
# def update_post(id: int, updated_post: Post):
#     index = find_index_post(id)
#     if index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id {id} does not exist")
#     post_data = updated_post.model_dump()
#     post_data["id"] = id
#     my_data[index] = post_data
#     return {"data": post_data}
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    index= find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    post_dict=post.model_dump()
    post_dict['id']=id
    my_data[index]=post_dict
    return {'data':my_data}