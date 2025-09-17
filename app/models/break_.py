from sqlalchemy import Integer, Column, DateTime, ForeignKey
from app.db.base import Base

class Break(Base):
    __tablename__ = 'breaks'
    id = Column(Integer, primary_key=True, index=True)
    start_datetime = Column(DateTime(timezone=True), nullable=False)
    end_datetime = Column(DateTime(timezone=True), nullable=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    shift_id = Column(Integer, ForeignKey('shifts.id'), nullable=True)