from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from . import schemas, database
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .config import settings
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_TIME = settings.access_token_expire_minutes

def create_access_token(data: dict):
  
  to_encode = data.copy()
  
  expire_time = datetime.now() + timedelta(ACCESS_TOKEN_EXPIRE_TIME)
  
  to_encode.update({"exp": expire_time})
  
  token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  
  return token


def verify_access_token(token: str, credentials_exeption):
  
  try:
    payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
    id: str = payload.get("user_id")
    role: str = payload.get("role")
    
    token_data = schemas.TokenData(id=id, role=role)
    
  except JWTError:
    raise credentials_exeption

  return token_data


def get_current_user(token: str = Depends(oauth2_scheme),
                    db : Session = Depends(database.get_db)):
  
  credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Could Not Validate Crendetials",
                                      headers={"WWW-Authenticate": "Bearer"})

  user_info = verify_access_token(token, credentials_exeption)
  
  return user_info

def get_optional_current_user(token: Optional[str] = Depends(oauth2_scheme_optional)):
    if not token:
        return None  # anonymous user, no token provided
    return get_current_user(token)