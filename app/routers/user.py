from fastapi import Body, FastAPI,Depends,status,HTTPException,Response,APIRouter
from .. import models,schemas,utils,oauth2
from ..database import get_db 
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    # hash the password-user.password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user with id {id} Not found")
    return user
    
    


