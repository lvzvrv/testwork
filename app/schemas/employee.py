from pydantic import BaseModel
from app.models.enums import Status, PositionEnum


class EmployeeCreate(BaseModel):
    last_name: str
    first_name: str
    patronymic: str
    position: PositionEnum

class EmployeeRead(BaseModel):
    id: int
    last_name: str
    first_name:str
    patronymic: str
    position: PositionEnum
    status: Status

    class Config:
        orm_mode: True