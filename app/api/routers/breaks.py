from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timezone
from typing import List
from app.db.session import get_session
from app.models.break_ import Break
from app.models.shift import Shift
from app.models.employee import Employee
from app.schemas.break_ import BreakCreate, BreakRead

router = APIRouter()


@router.post("/start", response_model=BreakRead)
async def start_break(break_data: BreakCreate, session: AsyncSession = Depends(get_session)):
    try:
        # Проверяем существование сотрудника
        employee = await session.get(Employee, break_data.employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # Проверяем, есть ли у сотрудника активный перерыв
        active_break_result = await session.execute(
            select(Break).where(
                Break.employee_id == break_data.employee_id,
                Break.end_datetime == None
            )
        )
        active_break = active_break_result.scalar_one_or_none()

        if active_break:
            raise HTTPException(
                status_code=400,
                detail="Employee already has an active break"
            )

        # Если не указана смена, ищем активную смену сотрудника
        shift_id = break_data.shift_id
        if not shift_id:
            active_shift_result = await session.execute(
                select(Shift).where(
                    Shift.employee_id == break_data.employee_id,
                    Shift.end_datetime == None
                )
            )
            active_shift = active_shift_result.scalar_one_or_none()

            if not active_shift:
                raise HTTPException(
                    status_code=400,
                    detail="Employee doesn't have an active shift"
                )

            shift_id = active_shift.id

        # Создаем новый перерыв
        break_ = Break(
            employee_id=break_data.employee_id,
            shift_id=shift_id,
            start_datetime=datetime.now(timezone.utc)
        )

        session.add(break_)
        await session.commit()
        await session.refresh(break_)

        return BreakRead.model_validate(break_)

    except Exception as e:
        await session.rollback()
        raise e


@router.post("/{break_id}/end", response_model=BreakRead)
async def end_break(break_id: int, session: AsyncSession = Depends(get_session)):
    try:
        break_ = await session.get(Break, break_id)

        if not break_:
            raise HTTPException(status_code=404, detail="Break not found")

        if break_.end_datetime:
            raise HTTPException(
                status_code=400,
                detail="Break already ended"
            )

        break_.end_datetime = datetime.now(timezone.utc)

        await session.commit()
        await session.refresh(break_)

        return BreakRead.model_validate(break_)

    except Exception as e:
        await session.rollback()
        raise e


@router.get("/", response_model=List[BreakRead])
async def get_breaks(session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Break))
        breaks = result.scalars().all()
        return [BreakRead.model_validate(break_) for break_ in breaks]

    except Exception as e:
        await session.rollback()
        raise e