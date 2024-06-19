from fastapi import APIRouter, Depends, status, Path
from fastapi.exceptions import HTTPException
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from .auth import get_current_user
from ..database import SessionLocal
from ..models import Users

# Changing password
from .auth import bcrypt_context
from pydantic import Field, BaseModel

router = APIRouter(
  prefix='/users', 
  tags=['users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db       
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency): 
  if user is None: 
    raise HTTPException(401, detail='Authentication Failed')
  user_model = db.query(Users).filter(Users.id == user.get('id')).first()
  if user_model is not None: 
    return user_model
  raise HTTPException(status_code=404, detail='User not found.')

class userVerification(BaseModel): 
  old_password: str
  new_password: str = Field(min_length=6)

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: userVerification): 
  if user is None: 
    raise HTTPException(401, detail='Authentication Failed')
  user_model = db.query(Users).filter(Users.id == user.get('id')).first()

  if not bcrypt_context.verify(user_verification.old_password, user_model.hashed_password): 
    raise HTTPException(401, detail='Error changing password')
  user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

  db.add(user_model)
  db.commit()

@router.put("/phone_number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: db_dependency, phone_number: str): 
  if user is None: 
    raise HTTPException(401, detail='Authentication Failed')
  user_model = db.query(Users).filter(Users.id == user.get('id')).first()
  user_model.phone_number = phone_number

  db.add(user_model)
  db.commit()

  
  

