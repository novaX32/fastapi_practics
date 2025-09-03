from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app=FastAPI()
class Address(BaseModel):
    city:str
    pincode:int

class gmail_user(BaseModel):
    id:int=Field(gt=0)
    name:str=Field(min_length=2,max_length=50)
    email:EmailStr
    age:int=Field(default=10,ge=18,le=100)
    


@app.get("/")
def root():
    return{"message":"yooo bitch"}

@app.post("/address")
def address(adddress:Address):
    print(adddress)
    print(adddress.model_dump() 
    )
    return{"message":adddress}



@app.post("/gmail_user")
def gmail_user(guser:gmail_user):
    print("User name: ",guser.name)
    print(guser.model_dump())
    return{"message":guser}


