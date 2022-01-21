from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key, algorithm, expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def createAccessToken(data: dict):
  toEncode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  toEncode.update({
    "exp": expire
  })
  encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
  
  return encodedJWT


def verifyAccessToken(token: str, credentialsException):
  # print("verifyAccessToken ", token)
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # extracting the data, getting specific field, in this case, user_id
    
    id: str = payload.get('userId')
    
    if id is None:
      raise credentialsException
    tokenData = schemas.TokenData(id = id)
    # print(tokenData)
  except JWTError:
    raise credentialsException
  
  return tokenData


# will pass this getCurrentUser() as a dependency into any of the path operations, it'll take the token from request automatically, extract the id, verify if the token is correct by calling the verifyAccessToken method

def getCurrentUser(token: str = Depends(oauth2_scheme)):
  credentialsException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
  # print('getCurrentUser ', token)
  
  return verifyAccessToken(token, credentialsException)
