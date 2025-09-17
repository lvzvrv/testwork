from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.enums import PositionEnum, Status

class ShiftBase(BaseModel):
    employee_id: int
    start_datetime: datetime
    end_datetime: Optional[datetime] = None

class ShiftCreate(BaseModel):
    employee_id: int

class ShiftUpdate(BaseModel):
    end_datetime: datetime

class ShiftRead(BaseModel):
    id: int
    employee_id: int
    start_datetime: datetime
    end_datetime: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)