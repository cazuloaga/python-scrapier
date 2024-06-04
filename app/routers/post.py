import math
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from .. import models,schemas, oauth2
from ..database import get_db
from sqlalchemy import func, or_

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# ORM get all
@router.get("/",status_code=status.HTTP_200_OK, response_model=schemas.PostPagination)
def get_post(db: Session = Depends(get_db), current_user =Depends(oauth2.get_current_user),page: int=1, limit:int=10):
    if limit>20:
        limit = 20
    if page == 0:
        page = 1
    skip = (page - 1) * limit
    posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).limit(limit).offset(skip).all()
    results= {'page': page,
        'page_size':len(posts),
        'data':posts}
    return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostPagination)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if current_user.active != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action. User status inactive")
    
    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

