import asyncio
from app.db.session import engine, AsyncSessionLocal
from app.db.base import Base
from app.models.employee import  Employee
from app.models.coefficient import Coefficient
from app.models.enums import Status, Parameter, CoefficientType, PositionEnum


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        emp = Employee(
            last_name='Ivanov',
            first_name='Ivan',
            patronymic='Ivanovich',
            position=PositionEnum.OPERATOR)
        session.add(emp)
        c1 = Coefficient(
            parameter=Parameter.TIME_TO_FIRST_ANSWER,
            norm=10.0,
            base=30.0,
            weight=0.5,
            type=CoefficientType.POSITIVE)
        c2 = Coefficient(
            parameter=Parameter.COMPETENCE,
            norm=5.0,
            base=3.0,
            weight=0.5,
            type=CoefficientType.POSITIVE)
        c3 = Coefficient(
            parameter=Parameter.ERRORS,
            norm=0.0,
            base=3.0,
            weight=1.0,
            type=CoefficientType.NEGATIVE)
        session.add_all([c1,c2,c3])
        await session.commit()

if __name__ == '__main__':
    asyncio.run(init_db())