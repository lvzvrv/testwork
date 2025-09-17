from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
import asyncio

from app.db.session import get_session
from app.models.salary_result import SalaryResult
from app.models.statistic import Statistic
from app.models.coefficient import Coefficient
from app.models.employee import Employee
from app.models.enums import Parameter, CoefficientType, Status
from app.schemas.salary_result import SalaryResultRead, SalaryResultCreate

router = APIRouter()

async def calculate_salary_for_employee(employee_id: int, period_start: datetime, period_end: datetime, session: AsyncSession):
    result = await session.execute(
        select(Statistic).where(
            Statistic.employee_id == employee_id,
            Statistic.date >= period_start,
            Statistic.date <= period_end
        )
    )
    statistics = result.scalars().all()

    result = await session.execute(select(Coefficient))
    coefficients = result.scalars().all()

    # group by param
    stats_by_parameter = {}
    for stat in statistics:
        if stat.parameter not in stats_by_parameter:
            stats_by_parameter[stat.parameter] = []
        stats_by_parameter[stat.parameter].append(stat.value)

    # avg values
    avg_values = {}
    for parameter, values in stats_by_parameter.items():
        avg_values[parameter] = sum(values) / len(values)

    pos_coefficient = 0.0
    neg_coefficient = 0.0
    details = {}

    for coeff in coefficients:
        if coeff.parameter in avg_values:
            avg_value = avg_values[coeff.parameter]

            if coeff.type == CoefficientType.POSITIVE:
                if avg_value <= coeff.norm:
                    param_coeff = 2.0
                elif avg_value >= coeff.base:
                    param_coeff = 1.0
                else:
                    param_coeff = 1.0 + (coeff.norm - avg_value) / (coeff.norm - coeff.base)

                pos_coefficient += param_coeff * coeff.weight
                details[coeff.parameter.value] = {   # <-- ключ как строка
                    "value": avg_value,
                    "coefficient": param_coeff,
                    "weight": coeff.weight,
                    "type": "positive"
                }

            elif coeff.type == CoefficientType.NEGATIVE:
                if avg_value <= coeff.norm:
                    param_coeff = 1.0
                elif avg_value >= coeff.base:
                    param_coeff = 0.0
                else:
                    param_coeff = 1.0 - (avg_value - coeff.norm) / (coeff.base - coeff.norm)

                neg_coefficient = param_coeff
                details[coeff.parameter.value] = {   # <-- ключ как строка
                    "value": avg_value,
                    "coefficient": param_coeff,
                    "type": "negative"
                }

    final_multiplier = pos_coefficient * neg_coefficient

    salary_result = SalaryResult(
        employee_id=employee_id,
        period_start=period_start,
        period_end=period_end,
        pos_coefficient=pos_coefficient,
        neg_coefficient=neg_coefficient,
        final_multiplier=final_multiplier,
        details=details   # <-- теперь JSON корректный
    )

    session.add(salary_result)
    await session.commit()
    await session.refresh(salary_result)
    return salary_result

@router.post('/calculate', response_model=List[SalaryResultRead])
async def calculate_salary(
        background_tasks = BackgroundTasks,
        period_start: datetime = None,
        period_end: datetime = None,
        session: AsyncSession = Depends(get_session)
):
    if not period_start or not period_end:
        now = datetime.now(timezone.utc)
        if not period_end:
            period_end = now.replace(day=1) - timedelta(days=1)
        if not period_start:
            period_start = period_end.replace(day=1)

    # all active employees
    result = await session.execute(select(Employee).where(
        Employee.status == Status.EMPLOYED
    ))
    employees = result.scalars().all()

    results = []
    for employee in employees:
        salary_result = await calculate_salary_for_employee(
            employee.id, period_start, period_end, session
        )
        results.append(salary_result)

    return [SalaryResultRead.model_validate(result) for result in results]

@router.get('/employee/{employee_id}', response_model=List[SalaryResultRead])
async def get_salary_results_by_employee(
        employee_id: int,
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(SalaryResult).where(SalaryResult.employee_id==employee_id)
    )
    salary_results = result.scalars().all()
    return [SalaryResultRead.model_validate(result) for result in salary_results]
