from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from app.db.base import Base
from app.models.enums import Status, PositionEnum


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    position = Column(Enum(PositionEnum), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.EMPLOYED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

