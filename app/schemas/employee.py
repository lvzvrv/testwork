from pydantic import BaseModel, ConfigDict
from app.models.enums import Status, PositionEnum
from typing import Optional

class EmployeeCreate(BaseModel):
    last_name: str
    first_name: str
    patronymic: str
    position: PositionEnum

class EmployeeRead(BaseModel):
    id: int
    last_name: str
    first_name: str
    patronymic: str
    position: PositionEnum
    status: Status

    model_config = ConfigDict(from_attributes=True)

class EmployeeUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    position: Optional[PositionEnum] = None
    status: Optional[Status] = None