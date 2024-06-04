from sqlalchemy import Column, ForeignKey,Integer,String,Boolean, Float, JSON, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# Model for table nameed post in db. 
# SQLalchemy wont modify tables if it finds a table named that way.
# Alembic for migration and changes
class User(Base):
    __tablename__='users'
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role_id = Column(Integer, nullable = False)
    active = Column(Boolean,server_default='TRUE',nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Website(Base):
    __tablename__='websites'
    id = Column(Integer,primary_key=True,nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    name = Column(String, nullable=False)
    website = Column(String, nullable=False)
    inner_type = Column(String, nullable=True) 
    inner_tag = Column(String, nullable=True)
    inner_type_value = Column(String, nullable=True)
    outer_type = Column(String, nullable=True) 
    outer_tag = Column(String, nullable=True)
    outer_type_value = Column(String, nullable=True)
    interest = Column(ARRAY(String))
    created_at= Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Post(Base):
    __tablename__='posts'
    id = Column(Integer,primary_key=True,nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=False) 
    relevance = Column(String, nullable=False)
    link_to_post = Column(String, nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


