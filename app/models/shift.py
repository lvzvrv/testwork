from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Shift(Base):
    __tablename__ = 'shifts'
    id = Column(Integer, primary_key=True, index=True)
    start_datetime = Column(DateTime(timezone=True), nullable=False)
    end_datetime = Column(DateTime(timezone=True), nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
