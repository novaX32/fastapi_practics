from fastapi import Body, FastAPI,Depends,status,HTTPException,Response,APIRouter
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List,Optional
from sqlalchemy import func

router=APIRouter(
    prefix="/post",
    tags=['Posts']
)

#Section3 ----------------------------------------------------------------------
# get all post
@router.get("/",response_model=List[schemas.PostOut])
# @router.get("/")

def get_data(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    print(limit)
    post=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #    post=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    # Convert tuples to dicts for FastAPI
    formatted_results = [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "published": post.published,
            "owner_id": post.owner_id,
            "votes": votes
        }
        for post, votes in results
    ]

    return formatted_results
    
   
    return results


# CREATE POST
# @app.post("/post", status_code=status.HTTP_201_CREATED)
# def create_post3(post: Post,db:Session=Depends(get_db)):
#     new_post=models.Post(title=post.title,content=post.content,published=post.published)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return {"new_data": new_post}
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post3(post: schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    print(current_user.id)
    print(current_user.email)
    new_post=models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# ---------------- GET POST BY ID -----------------
@router.get("/{id}", response_model=schemas.PostOut)
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Query the Post along with vote count
    results = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {id} not found"
        )

    post, votes = results  # Unpack tuple
    # Convert to dict compatible with PostOut
    formatted_post = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "published": post.published,
        "owner_id": post.owner_id,
        "votes": votes
    }

    return formatted_post   

   
   
   


# Delete post by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    if post.owner_id!=current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="this acttion is not authorized bich!!"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    existing_post=post_query.first()
    
    if existing_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    if existing_post.owner_id!=current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="this acttion is not authorized bich!!"
        )
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()




# SECTION 1 --------------------------------------------------------->
# @app.post("/create")
# def create_post():
#     return{"message":"successfully created posts"}


# @app.post("/secondpost")
# def create_post2(payload: dict=Body(...)):
#     print(payload)
#     return{"new_post":f"title {payload['title']} content: {payload['content']}"}

#what data we want for a specific post request
#we want a title str
#content str
#we just want this two things we dont expect the user should 
#send anything else

#fast api will automatically validate the data the 
# #we have received from the client and validate it 
# does it have title if so is it a string,content if so is it a string
# #if no it will throw an erroe 

# SECTION 2 --------------------------------------------------------------------->
# @app.get("/post")
# def get_data():
#     cursor.execute("""SELECT *FROM posts""")
#     posts=cursor.fetchall()
#     print(posts)
#     return{"Data":posts}

# @app.get("/post/{id}")
# def get_post_by_id(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
#     get_post = cursor.fetchone()
#     if not get_post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with ID: {id} was not found"
#         )
#     return {"data": get_post}

# @app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id=%s returning *""",(id,))
#     delete_post=cursor.fetchone()
#     conn.commit()
#     if delete_post==None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail=f"Post with id {id} does not exist")
 
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/post/{id}")
# def update_post(id:int,post:Post):
#     cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s returning *""",(post.title,post.content,post.published,id))
#     updated_post=cursor.fetchone()
#     conn.commit()
#     if updated_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id {id} does not exist")
    
#     return {'data':updated_post}



    




