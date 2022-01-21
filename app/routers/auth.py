from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas, utils

router = APIRouter(
  tags=['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
  # SQLAlchemy ORM method
  user = db.query(models.User).filter(models.User.email == userCredentials.username).first()
  
  if not user:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail=f"Invalid Credentials")
      
  if not utils.verify(userCredentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail=f"Invalid Credentials")
  
  # creating jwt token
  
  accessToken = oauth2.createAccessToken(data={
    "userId": user.id
  })
  return {
    "accessToken": accessToken,
    "token_type": "bearer"
  }
