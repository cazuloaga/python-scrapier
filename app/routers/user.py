from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2
from ..database import get_db
from sqlalchemy import func
from typing import List

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

#ORM create user
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate ,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if current_user.role_id != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#ORM get user
@router.get("/{id}", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def get_user(id: int ,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if current_user.id != id or current_user.role_id != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} does not exist')
    

    return user


    
