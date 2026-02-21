from pydantic import BaseModel, EmailStr
from typing import Literal, Optional, List
from datetime import datetime


class RoleOut(BaseModel):
  name: str

#Users
class UserCreate(BaseModel):
  full_name: str
  email: EmailStr
  phone_num: str
  password: str
  role: Optional[str] = "user"

class UserResponse(BaseModel):
  id: int
  full_name: str
  email: EmailStr
  phone_num: str
  created_at: datetime
  role: RoleOut


#Authetication
class UserLogin(BaseModel):
  email: EmailStr
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: int
  role: Literal["admin", "staff", "user"]
