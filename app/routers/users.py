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
            current_user: dict = Depends(oauth2.get_optional_current_user)):
  
  # If trying to create admin or staff, must be authenticated and be an admin
  if user.role in ("admin", "staff"):
    if current_user is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                          detail="Authentication required")
    if current_user.role != "admin":
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                          detail="Admin privileges required")

  # receiving role id
  role = db.query(models.Role).filter(models.Role.name == user.role).first()
  if role is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Role Not Found")

  #hashing password
  user.password = utils.hash(user.password)
  
  #prepare user model
  user_dict = {k: v for k, v in user.dict().items() if k != "role"}
  user_dict["role_id"] = role.id
  new_user = models.User(**user_dict)
  
  #Verify that the email is unique
  try:
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
  except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail="Email Already exist")
  return new_user

