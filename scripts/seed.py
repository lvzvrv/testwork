import sys
import os
import asyncio
from datetime import datetime, timedelta, timezone

# Добавляем корневую директорию проекта в Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine, AsyncSessionLocal
from app.db.base import Base
from app.models.employee import Employee
from app.models.coefficient import Coefficient
from app.models.shift import Shift
from app.models.statistic import Statistic
from app.models.enums import PositionEnum, Status, Parameter, CoefficientType
from sqlalchemy import select


async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже коэффициенты
        result = await session.execute(select(Coefficient))
        if result.scalars().first():
            print("Коэффициенты уже заполнены. Пропускаем.")
        else:
            # Создаем коэффициенты
            coefficients = [
                # Положительные коэффициенты
                Coefficient(
                    parameter=Parameter.TIME_TO_FIRST_ANSWER,
                    norm=10.0,
                    base=30.0,
                    weight=0.25,
                    type=CoefficientType.POSITIVE,
                    note="Время ответа на первое сообщение (секунды)"
                ),
                Coefficient(
                    parameter=Parameter.TIME_TO_NEXT_ANSWER,
                    norm=5.0,
                    base=15.0,
                    weight=0.25,
                    type=CoefficientType.POSITIVE,
                    note="Время ответа на последующие сообщения (секунды)"
                ),
                Coefficient(
                    parameter=Parameter.COMPETENCE,
                    norm=5.0,
                    base=3.0,
                    weight=0.25,
                    type=CoefficientType.POSITIVE,
                    note="Оценка компетентности (баллы)"
                ),
                Coefficient(
                    parameter=Parameter.POLITENESS,
                    norm=5.0,
                    base=3.0,
                    weight=0.25,
                    type=CoefficientType.POSITIVE,
                    note="Оценка вежливости (баллы)"
                ),
                # Негативный коэффициент
                Coefficient(
                    parameter=Parameter.ERRORS,
                    norm=0.0,
                    base=5.0,
                    weight=1.0,
                    type=CoefficientType.NEGATIVE,
                    note="Количество ошибок"
                )
            ]

            session.add_all(coefficients)
            print("Коэффициенты успешно добавлены.")

        # Проверяем, есть ли уже сотрудники
        result = await session.execute(select(Employee))
        if result.scalars().first():
            print("Сотрудники уже созданы. Пропускаем.")
        else:
            # Создаем тестовых сотрудников
            employees = [
                Employee(
                    last_name="Иванов",
                    first_name="Иван",
                    patronymic="Иванович",
                    position=PositionEnum.MANAGER,
                    status=Status.EMPLOYED
                ),
                Employee(
                    last_name="Петров",
                    first_name="Петр",
                    patronymic="Петрович",
                    position=PositionEnum.OPERATOR,
                    status=Status.EMPLOYED
                ),
                Employee(
                    last_name="Сидорова",
                    first_name="Анна",
                    patronymic="Владимировна",
                    position=PositionEnum.SENIOR,
                    status=Status.EMPLOYED
                )
            ]

            session.add_all(employees)
            await session.commit()
            print("Тестовые сотрудники успешно добавлены.")

        # Получаем всех сотрудников для создания смен и статистики
        result = await session.execute(select(Employee))
        employees = result.scalars().all()

        # Создаем тестовые смены (за последние 30 дней)
        for employee in employees:
            # Проверяем, есть ли уже смены для сотрудника
            result = await session.execute(
                select(Shift).where(Shift.employee_id == employee.id)
            )
            if not result.scalars().first():
                # Создаем несколько смен за последние 30 дней
                for i in range(5):
                    start_time = datetime.now(timezone.utc) - timedelta(days=30 - i * 2)
                    end_time = start_time + timedelta(hours=8)

                    shift = Shift(
                        employee_id=employee.id,
                        start_datetime=start_time,
                        end_datetime=end_time
                    )
                    session.add(shift)

        await session.commit()
        print("Тестовые смены созданы.")

        # Получаем все смены для создания статистики
        result = await session.execute(select(Shift))
        shifts = result.scalars().all()

        # Создаем тестовую статистику
        for shift in shifts:
            # Проверяем, есть ли уже статистика для смены
            result = await session.execute(
                select(Statistic).where(Statistic.shift_id == shift.id)
            )
            if not result.scalars().first():
                # Создаем статистику для каждой смены
                statistics = [
                    Statistic(
                        parameter=Parameter.TIME_TO_FIRST_ANSWER,
                        value=15.5,  # Между norm (10) и base (30)
                        employee_id=shift.employee_id,
                        shift_id=shift.id,
                        date=shift.start_datetime
                    ),
                    Statistic(
                        parameter=Parameter.TIME_TO_NEXT_ANSWER,
                        value=8.0,  # Между norm (5) и base (15)
                        employee_id=shift.employee_id,
                        shift_id=shift.id,
                        date=shift.start_datetime
                    ),
                    Statistic(
                        parameter=Parameter.COMPETENCE,
                        value=4.2,  # Между base (3) и norm (5)
                        employee_id=shift.employee_id,
                        shift_id=shift.id,
                        date=shift.start_datetime
                    ),
                    Statistic(
                        parameter=Parameter.POLITENESS,
                        value=4.5,  # Между base (3) и norm (5)
                        employee_id=shift.employee_id,
                        shift_id=shift.id,
                        date=shift.start_datetime
                    ),
                    Statistic(
                        parameter=Parameter.ERRORS,
                        value=2.0,  # Между norm (0) и base (5)
                        employee_id=shift.employee_id,
                        shift_id=shift.id,
                        date=shift.start_datetime
                    )
                ]
                session.add_all(statistics)

        await session.commit()
        print("Тестовая статистика успешно добавлена.")

        print("Все данные успешно заполнены.")


if __name__ == "__main__":
    asyncio.run(seed_data())