from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.routers import employees

app = FastAPI(title='Salary Service')
app.include_router(employees.router, prefix='/employees', tags=['employees'])

# Создание таблиц на старт апе, в проде сделать Alembic
@app.on_event('startup')
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)