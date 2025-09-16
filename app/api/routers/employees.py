from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.employee import EmployeeRead, EmployeeCreate
from app.db.session import get_session
from app.models.employee import Employee

router = APIRouter()

@router.post('/', response_model=EmployeeRead)
async def create_employee(payload: EmployeeCreate, session: AsyncSession = Depends(get_session)):
    emp = Employee(
        last_name = payload.last_name,
        first_name = payload.first_name,
        patronymic = payload.patronymic,
        position = payload.position,
    )
    session.add(emp)
    await session.commit()
    await session.refresh(emp)
    return emp

