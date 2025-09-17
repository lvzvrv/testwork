from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.db.session import get_session
from app.models.coefficient import Coefficient
from app.schemas.coefficient import CoefficientRead, CoefficientCreate, CoefficientUpdate

router = APIRouter()

@router.post('/', response_model=CoefficientRead)
async def create_coefficient(coefficient_data: CoefficientCreate, session: AsyncSession = Depends(get_session)):
    try:
        existing_coefficient = await session.execute(
            select(Coefficient).where(
                Coefficient.parameter==coefficient_data.parameter,
                Coefficient.type==coefficient_data.type
            )
        )
        if existing_coefficient:
            raise HTTPException(
                status_code=400,
                detail="Coefficient for this parameter and type are already exists"
            )

        coefficient = Coefficient(**coefficient_data.model_dump())
        session.add(coefficient)
        await session.commit()
        await session.refresh(coefficient)

        return CoefficientRead.model_validate(coefficient)

    except Exception as e:
        await session.rollback()
        raise e

@router.get('/', response_model=List[CoefficientRead])
async def get_coefficients(session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Coefficient))
        coefficients = result.scalars().all()
        return [CoefficientRead.model_validate(coeff) for coeff in coefficients]

    except Exception as e:
        await session.rollback()
        raise e

@router.get('/{coefficient_id}', response_model=CoefficientRead)
async def get_coefficient(coefficient_id: int, session: AsyncSession = Depends(get_session)):
    try:
        coefficient = await session.get(Coefficient, coefficient_id)
        if not coefficient:
            raise HTTPException(
                status_code=404,
                detail="Coefficient not found"
            )

        return CoefficientRead.model_validate(coefficient)

    except Exception as e:
        await session.rollback()
        raise e

@router.put('/{coefficient_id}', response_model=CoefficientRead)
async def update_coefficient(coefficient_id: int, coefficient_data: CoefficientUpdate, session: AsyncSession = Depends(get_session)):
    try:
        coefficient = await session.get(Coefficient, coefficient_id)
        if not coefficient:
            raise HTTPException(
                status_code=404,
                detail="Coefficient not found"
            )

        update_data = coefficient_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(coefficient, field, value)

        await session.commit()
        await session.refresh(coefficient)

        return CoefficientRead.model_validate(coefficient)

    except Exception as e:
        await session.rollback()
        raise e

@router.delete('/{coefficient_id}')
async def delete_coefficient(coefficient_id: int, session: AsyncSession = Depends(get_session)):
    try:
        coefficient = await session.get(Coefficient, coefficient_id)
        if not coefficient:
            raise HTTPException(
                status_code=404,
                detail="Coefficient not found"
            )

        await session.delete(coefficient)
        await session.commit()

        return {"message": "Coefficient deleted successfully"}

    except Exception as e:
        await session.rollback()
        raise e
