from sqlalchemy import Column, Integer, Float, Enum, String
from sqlalchemy.sql.cache_key import CACHE_IN_PLACE

from app.db.base import Base
from app.models.enums import Parameter, CoefficientType

class Coefficient(Base):
    __tablename__ = 'coefficients'
    id = Column(Integer, primary_key=True, index = True)
    parameter = Column(Enum(Parameter), nullable=False)
    norm = Column(Float, nullable=False)
    base = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    type = Column(Enum(CoefficientType), nullable=False)
    note = Column(String, nullable=True)

    