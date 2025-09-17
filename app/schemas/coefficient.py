from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.enums import Parameter, CoefficientType

class CoefficientBase(BaseModel):
    parameter: Parameter
    norm: float
    base: float
    weight: float
    type: CoefficientType
    note: Optional[str] = None

class CoefficientCreate(CoefficientBase):
    pass

class CoefficientRead(CoefficientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class CoefficientUpdate(BaseModel):
    norm: Optional[float] = None
    base: Optional[float] = None
    weight: Optional[float] = None
    note: Optional[str] = None