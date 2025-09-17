from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.db.session import get_session
from app.models.statistic import Statistic
from app.models.employee import Employee
from app.models.shift import Shift
from app.schemas.statistic import StatisticRead, StatisticCreate

router = APIRouter()


@router.post("/", response_model=StatisticRead)
async def create_statistic(statistic_data: StatisticCreate, session: AsyncSession = Depends(get_session)):
    try:
        employee = await session.get(Employee, statistic_data.employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        if statistic_data.shift_id:
            shift = await session.get(Shift, statistic_data.shift_id)
            if not shift:
                raise HTTPException(status_code=404, detail="Shift not found")

        statistic = Statistic(**statistic_data.model_dump())
        session.add(statistic)
        await session.commit()
        await session.refresh(statistic)

        return StatisticRead.model_validate(statistic)

    except Exception as e:
        await session.rollback()
        raise e


@router.get("/", response_model=List[StatisticRead])
async def get_statistics(session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Statistic))
        statistics = result.scalars().all()
        return [StatisticRead.model_validate(stat) for stat in statistics]

    except Exception as e:
        await session.rollback()
        raise e


@router.get("/employee/{employee_id}", response_model=List[StatisticRead])
async def get_statistics_by_employee(employee_id: int, session: AsyncSession = Depends(get_session)):
    try:
        # Проверяем существование сотрудника
        employee = await session.get(Employee, employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        result = await session.execute(
            select(Statistic).where(Statistic.employee_id == employee_id)
        )
        statistics = result.scalars().all()
        return [StatisticRead.model_validate(stat) for stat in statistics]

    except Exception as e:
        await session.rollback()
        raise e


@router.get("/{statistic_id}", response_model=StatisticRead)
async def get_statistic(statistic_id: int, session: AsyncSession = Depends(get_session)):
    try:
        statistic = await session.get(Statistic, statistic_id)
        if not statistic:
            raise HTTPException(status_code=404, detail="Statistic not found")

        return StatisticRead.model_validate(statistic)

    except Exception as e:
        await session.rollback()
        raise e