from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime

#Users

class UserCreate(BaseModel):
  full_name: int
  email: EmailStr
  phone_num: str
  password: str

class UserResponse(BaseModel):
  id: int
  full_name: int
  email: EmailStr
  phone_num: str
  password: str
  created_at: datetime



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
