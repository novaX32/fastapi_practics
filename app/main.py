from fastapi import Body, FastAPI
from . import models
from .database import engine
from . routers import user,post,auth,vote
from fastapi.middleware.cors import CORSMiddleware
from .config import settings


# models.Base.metadata.create_all(bind=engine)

app=FastAPI()
#  origins=["https://www.google.com"]
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return{"message":"hello Im OptimusPrime"}











my_data=[{"id":1,"name":"Aarya","roll_no":28},{"id":2,"name":"Nikhil","roll_no":29},{"id":3,"name":"Mahesh","roll_no":30}]







