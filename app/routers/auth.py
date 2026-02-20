from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils

router = APIRouter(
  prefix="/login",
  tags=["Authentication"]
)

@router.post("/",
            response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db),):
  
  user = (db.query(models.User)
          .filter(models.User.email == user_credentials.username)
          .first())
  
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid Credentials")
  
  if not utils.verify(user_credentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid Credentials")
  
  data = {"user_id": user.id, "role": user.role}
  
  return access_token(user_credentials)