# For sqlachemy to understand what kind of tables we'll be creating within the database in the future

# Table that is being stored in database
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(Base):
    # Create a new table, name is 'users'
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    # each user has a unique email and username
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String) 
    phone_number = Column(String)



class Todos(Base):
    __tablename__ = 'todos'     # for sqls to understand what to name this table inside database

    id = Column(Integer, primary_key=True, index=True)  # primary key will be unique; index means idnex is increatable, indexible => unique
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    # when the user logs in, we grab primary key, and all the todos matched with user.id
    owner_id = Column(Integer, ForeignKey("users.id")) # The FK(Foreign Key) to User's ID
