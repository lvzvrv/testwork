from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timezone
from typing import List
from app.db.session import get_session
from app.models.shift import Shift
from app.schemas.shift import ShiftCreate, ShiftRead
from app.models.employee import Employee

router = APIRouter()


@router.post("/start", response_model=ShiftRead)
async def start_shift(shift_data: ShiftCreate, session: AsyncSession = Depends(get_session)):
    try:
        employee = await session.get(Employee, shift_data.employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        active_shift_result = await session.execute(
            select(Shift).where(
                Shift.employee_id == shift_data.employee_id,
                Shift.end_datetime == None
            )
        )
        active_shift = active_shift_result.scalar_one_or_none()

        if active_shift:
            raise HTTPException(
                status_code=400,
                detail="Employee already has an active shift"
            )

        shift = Shift(
            employee_id=shift_data.employee_id,
            start_datetime=datetime.now(timezone.utc)
        )

        session.add(shift)
        await session.commit()
        await session.refresh(shift)

        return ShiftRead.model_validate(shift)

    except Exception as e:
        await session.rollback()
        raise e


@router.post("/{shift_id}/end", response_model=ShiftRead)
async def end_shift(shift_id: int, session: AsyncSession = Depends(get_session)):
    try:
        shift = await session.get(Shift, shift_id)

        if not shift:
            raise HTTPException(status_code=404, detail="Shift not found")

        if shift.end_datetime:
            raise HTTPException(
                status_code=400,
                detail="Shift already ended"
            )

        shift.end_datetime = datetime.now(timezone.utc)

        await session.commit()
        await session.refresh(shift)

        return ShiftRead.model_validate(shift)

    except Exception as e:
        await session.rollback()
        raise e


@router.get("/", response_model=List[ShiftRead])
async def get_shifts(session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Shift))
        shifts = result.scalars().all()
        return [ShiftRead.model_validate(shift) for shift in shifts]

    except Exception as e:
        await session.rollback()
        raise e