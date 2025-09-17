from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any

class SalaryResultBase(BaseModel):
    employee_id: int
    period_start: datetime
    period_end: datetime
    pos_coefficient: Optional[float] = None
    neg_coefficient: Optional[float] = None
    final_multiplier: float
    details: Optional[Dict[str, Any]] = None

class SalaryResultCreate(SalaryResultBase):
    pass

class SalaryResultRead(SalaryResultBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)