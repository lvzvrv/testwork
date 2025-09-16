from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.sql.traversals import ColIdentityComparatorStrategy

from app.db.base import Base
from app.models.enums import Parameter

class Statistic(Base):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    parameter = Column(Enum(Parameter), nullable = False)
    value = Column(Float, nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    shift_id = Column(Integer, ForeignKey('shifts.id'), nullable=True)

