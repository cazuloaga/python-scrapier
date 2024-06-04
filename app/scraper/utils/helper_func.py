from sqlalchemy.orm import Session
from app import models, schemas

def check_post_exists(db:Session, current_user: int, url: str):
    posts=db.query(models.Post).filter(models.Post.owner_id==current_user,
                                       models.Post.link_to_post==url).all()
    return posts != []
