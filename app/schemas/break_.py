from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class BreakBase(BaseModel):
    employee_id: int
    shift_id: Optional[int] = None
    start_datetime: datetime
    end_datetime: Optional[datetime] = None

class BreakCreate(BaseModel):
    employee_id: int
    shift_id: Optional[int] = None

class BreakUpdate(BaseModel):
    end_datetime: datetime

class BreakRead(BaseModel):
    id: int
    employee_id: int
    shift_id: Optional[int] = None
    start_datetime: datetime
    end_datetime: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)