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
  
class UserUpdate(UserCreate):
  pass

class UserResponse(BaseModel):
  id: int
  full_name: str
  email: EmailStr
  phone_num: str
  created_at: datetime
  role: RoleOut


#Appointments

class AppointmentCreate(BaseModel):
  service: str
  status: Literal["pending", "paid"]
  start_date_time: datetime
  staff_notes: Optional[str] = None
  cancelation_reason: Optional[str] = None


class AppointmentResponse(BaseModel):
  id: int
  service_id: int
  status: Literal["pending", "paid"]
  start_date_time: datetime
  end_date_time: datetime
  staff_notes: Optional[str] = None
  cancelation_reason: Optional[str] = None
  created_at: datetime
  updated_at: datetime
  
  user: UserResponse


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
