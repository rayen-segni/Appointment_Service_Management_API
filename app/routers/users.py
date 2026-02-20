from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, models, oauth2, utils

router = APIRouter(
  prefix="/users",
  tags=["Users"]
)

@router.post("/",
            response_model=schemas.UserResponse,
            status_code=status.HTTP_201_CREATED)
def add_user(user: schemas.UserCreate,
            db: Session = Depends(get_db),
            current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
  
  #verify on privileges
  # if not(current_user.role == "admin" or current_user.role == "staff"):
  #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
  #                       detail="Some Privileges Required")
  
  #hashing password
  user.password = utils.hash(user.password)
  
  #prepare user model
  new_user = models.User(**user.dict())
  
  #Verify taht the email is unique
  try:
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
  except IntegrityError:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail="Email Already exist")
  
  return new_user

