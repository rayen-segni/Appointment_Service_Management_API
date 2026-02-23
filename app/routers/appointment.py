from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas, oauth2, models
from datetime import datetime, timedelta

router = APIRouter(
  prefix="/appointments",
  tags=["Appointments"]
)

@router.post("/",
            
            status_code=status.HTTP_201_CREATED)
def add_appointment(appointment : schemas.AppointmentCreate,
                    db: Session = Depends(get_db)):
  
  service = (db.query(models.Service)
            .filter(models.Service.name == appointment.service)
            .first())
  
  if service is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Service Name Not Found")
  
  exist_appoint = (db.query(models.Appointment)
                  .filter(models.Appointment.start_date_time == appointment.start_date_time)
                  .first())
  
  if exist_appoint :
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="You already have an appointment with this date and time")
  
  
  appoint_dict = {k: v for k, v in appointment.dict().items() if k != "service"}
  
  appoint_dict.update({"service_id": service.id})
  appoint_dict["status"] = appoint_dict["status"].upper()
  
  end_date_time = appointment.start_date_time + timedelta(hours=service.duration)
  appoint_dict.update({"end_date_time": end_date_time})
  
  #need to fix current user verification
  new_appoint = models.Appointment(user_id=16, **appoint_dict)
  
  db.add(new_appoint)
  db.commit()
  db.refresh(new_appoint)
  
  return new_appoint

