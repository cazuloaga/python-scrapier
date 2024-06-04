from typing import List, Optional, Dict
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: int
    class Config:
        from_attributes=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id:str
    name: str
    email: EmailStr
    created_at:datetime
    class Config:
        from_attributes=True

class Website(BaseModel):
    name: str
    website: str
    inner_type: Optional[str] = None
    inner_tag: Optional[str] = None
    inner_type_value: Optional[str] = None
    outer_type: Optional[str] = None
    outer_tag: Optional[str] = None
    outer_type_value: Optional[str] = None
    interest: Optional[List[str]] = []

class WebsiteOut(Website):
    owner_id: int
    id: int

class PostCreate(BaseModel):
    link_to_post: str

class PostCreateAuto(BaseModel):
    owner_id: int
    title : str
    summary: str
    relevance: str
    link_to_post: str

class PostOut(PostCreate):
    id: int
    title: str
    summary: str
    relevance: str

class Pagination(BaseModel):
    page: int
    page_size: int
    class Config:
        from_attributes=True

class WebsitePagination(Pagination):
    data: List[WebsiteOut]

class PostPagination(Pagination):
    data: List[PostOut]

class Token(BaseModel):
    logged: bool
    detail: str
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None







