from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router=APIRouter(
    tags=['Authentication']
)

@router.post('/login',response_model=schemas.Token)
# OAuth2PasswordRequestForm is a FastAPI class used for handling OAuth2 login forms (username + password).
# Depends() tells FastAPI to automatically extract the form data from the request and provide it to this function.
# So when a client sends a POST request with username and password (form data), FastAPI will populate user_credentials with:
# user_credentials.username  # The username sent in the form
# user_credentials.password  # The password sent in the form

def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
   user= db.query(models.User).filter(models.User.email==user_credentials.username).first()
   if not user:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials" )
   
   if not utils.verify(user_credentials.password,user.password):
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
   
   #CREATE TOKEN
   access_token=oauth2.create_access_token(data={"user_id":user.id})

   #return token
   return{"access_token":access_token,"token_type":"beare"}
      

    