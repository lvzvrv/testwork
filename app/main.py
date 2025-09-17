from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.routers import employees, shifts, breaks, statistic, coefficients, salary

app = FastAPI(title='Salary Service')
app.include_router(employees.router, prefix='/employees', tags=['employees'])
app.include_router(shifts.router, prefix='/shifts', tags=['shifts'])
app.include_router(breaks.router, prefix='/breaks', tags=['breaks'])
app.include_router(coefficients.router, prefix='/coefficients', tags=['coefficients'])
app.include_router(statistic.router, prefix='/statistics', tags=['statistics'])
app.include_router(salary.router, prefix='/salary', tags=['salary'])

# Создание таблиц на старт апе, в проде сделать Alembic
@app.on_event('startup')
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)