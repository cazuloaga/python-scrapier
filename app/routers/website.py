import math
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from .. import models,schemas, oauth2
from ..database import get_db
from ..scraper.scrape_websites import scrape_website

from sqlalchemy import func, or_

router=APIRouter(
    prefix="/websites",
    tags=['Websites']
)

# ORM get all
@router.get("/",status_code=status.HTTP_200_OK, response_model=schemas.WebsitePagination)
def get_websites(db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user),page: int=1, limit:int=10):
    uid=current_user.id
    websites=db.query(models.Website).filter(models.Website.owner_id==uid).all()
    total_items=len(websites)        
    results= {'page': page,
        'total_items':total_items,
        'total_pages': math.ceil(total_items/limit),
        'page_size':limit,
        'data':websites}
    return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Website)
def create_website(website: schemas.Website, db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if current_user.active != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action. User status inactive")
    
    new_website=models.Website(**website.model_dump())
    new_website.owner_id = current_user.id
    
    db.add(new_website)
    db.commit()
    db.refresh(new_website)
    return new_website

@router.post("/scrape_website/{website_id}",status_code=status.HTTP_201_CREATED,response_model=list)
def create_website(website_id: int, db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if current_user.active != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action. User status inactive")
    website = db.query(models.Website).filter(models.Website.owner_id==current_user.id,
                                              models.Website.id==website_id).first()
    if not website:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"No website found with id: {website_id}")
    results = scrape_website(website, db)
    for result in results:
        new_post=models.Post(**result)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

    return results

@router.put("/{id}", response_model=schemas.Website)
def update_website(id: int, updated_website: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    website_query = db.query(models.Website).filter(models.Website.id == id)

    website = website_query.first()

    if website == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"website with id: {id} does not exist")
    if website.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    website_query.update(updated_website.model_dump(), synchronize_session=False)

    db.commit()

    return website_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_website(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    website_query = db.query(models.Post).filter(models.Post.id == id)

    website = website_query.first()

    if website == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"website with id: {id} does not exist")

    if website.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    website_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

