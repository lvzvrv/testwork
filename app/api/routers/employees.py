from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.employee import EmployeeRead, EmployeeCreate, EmployeeUpdate
from app.db.session import get_session
from app.models.employee import Employee

router = APIRouter()


@router.post('/', response_model=EmployeeRead)
async def create_employee(payload: EmployeeCreate, session: AsyncSession = Depends(get_session)):
    employee = Employee(
        last_name=payload.last_name,
        first_name=payload.first_name,
        patronymic=payload.patronymic,
        position=payload.position,
    )
    session.add(employee)
    await session.commit()
    await session.refresh(employee)
    return employee


@router.get('/', response_model=List[EmployeeRead])
async def get_employees(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Employee))
    employees = result.scalars().all()
    return [EmployeeRead.model_validate(employee) for employee in employees]


@router.get('/{employee_id}', response_model=EmployeeRead)
async def get_employee(employee_id: int, session: AsyncSession = Depends(get_session)):
    employee = await session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeRead.model_validate(employee)


@router.put('/{employee_id}', response_model=EmployeeRead)
async def update_employee(employee_id: int, payload: EmployeeUpdate, session: AsyncSession = Depends(get_session)):
    employee = await session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)

    await session.commit()
    await session.refresh(employee)
    return EmployeeRead.model_validate(employee)


@router.delete('/{employee_id}')
async def delete_employee(employee_id: int, session: AsyncSession = Depends(get_session)):
    employee = await session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    await session.delete(employee)
    await session.commit()
    return {"message": "Employee deleted successfully"}