from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.enums import Parameter

class StatisticBase(BaseModel):
    parameter: Parameter
    value: float
    employee_id: int
    shift_id: Optional[int] = None

class StatisticCreate(StatisticBase):
    pass

class StatisticRead(StatisticBase):
    id: int
    date: datetime

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )