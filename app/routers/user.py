from typing import List

from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
  prefix="/users",
  tags=['Users']
)

# CREATE USER STARTS

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def createUser(user: schemas.CreateUser, db: Session = Depends(get_db)):
  # hashing the password - user.password
  hashedPassword = utils.hash(user.password)
  user.password = hashedPassword
  
  # models -> db table class
  newUser = models.User(**user.dict())
  db.add(newUser)
  db.commit()
  db.refresh(newUser)
  return newUser

# CREATE USER ENDS


# GET USER BY ID STARTS

@router.get("/{id}", response_model=schemas.UserResponse)
def getUser(id: int, db: Session = Depends(get_db)):
  # SQLAlchemy ORM method
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"user with {id} not found")
  return user

# GET USER BY ID ENDS
