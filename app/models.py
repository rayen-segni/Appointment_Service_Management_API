from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Float, Interval, Enum, DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum


class AppointStatus(enum.Enum):
  PENDING = "pending"
  PAID = "paid"
  CANCELED = "canceled"

#Role Model
class Role(Base):
  __tablename__ = "roles"
  
  id = Column(Integer, primary_key=True, nullable=False)
  name = Column(String, unique=True, nullable=False)


#User Model
class User(Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True, nullable=False)
  full_name = Column(String, nullable=False)
  email = Column(String, unique=True, nullable=False)
  phone_num = Column(String, nullable=False)
  role_id = Column(Integer, ForeignKey(Role.id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True)
  password = Column(String, nullable=False)
  created_at = Column(DateTime, server_default=func.now(), nullable=False)
  
  role = relationship("Role")
  



#Role of each user
class UserRole(Base):
  __tablename__ = "user_roles"
  
  user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable=False, index=True)
  role_id = Column(Integer, ForeignKey(Role.id, ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable=False)

  user = relationship("User")
  role = relationship("Role")


#Permession Model
class Permession(Base):
  __tablename__ = "permessions"
  
  id = Column(Integer, primary_key=True, nullable=False)
  name = Column(String, unique=True, nullable=False)
  description = Column(String)


#Permession of each role
class RolePermession(Base):
  __tablename__ = "role_permessions"
  
  permession_id = Column(Integer, ForeignKey(Permession.id, ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable=False)
  role_id = Column(Integer, ForeignKey(Role.id, ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable=False)

  permission= relationship("Permession")
  role = relationship("Role")


#Service Model
class Service(Base):
  __tablename__ = "services"
  
  id = Column(Integer, primary_key=True, nullable=False)
  staff_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
  name = Column(String, unique=True, nullable=False)
  price = Column(Float, nullable=False)
  duration = Column(Integer, nullable=False)
  description = Column(String)


#Appointment Model
class Appointment (Base):
  __tablename__ = "appointments"
  
  id = Column(Integer, primary_key=True, nullable=False)
  user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
  service_id = Column(Integer, ForeignKey(Service.id, ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
  status = Column(Enum(AppointStatus), nullable=False, default=AppointStatus.PENDING)
  
  start_time = Column(DateTime, nullable=False)
  end_time = Column(DateTime, nullable=False)
  
  created_at = Column(DateTime, nullable=False, server_default=func.now())
  updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
  cancelled_at = Column(DateTime, nullable=True)

  staff_notes = Column(String, nullable=True)
  cancelation_reason = Column(String, nullable=True)
  
  user = relationship("User")
  service = relationship("Service")


