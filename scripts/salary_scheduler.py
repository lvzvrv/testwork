import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from datetime import datetime, timezone, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.future import select

from app.db.session import AsyncSessionLocal
from app.models.employee import Employee
from app.models.enums import Status
from app.api.routers.salary import calculate_salary_for_employee


async def monthly_salary_job():
    async with AsyncSessionLocal() as session:
        now = datetime.now(timezone.utc)
        # конец периода — последний день прошлого месяца
        period_end = now.replace(day=1) - timedelta(days=1)
        period_start = period_end.replace(day=1)

        result = await session.execute(
            select(Employee).where(Employee.status == Status.EMPLOYED)
        )
        employees = result.scalars().all()

        print(f"[{datetime.now()}] Начало расчёта зарплаты для {len(employees)} сотрудников")

        for employee in employees:
            await calculate_salary_for_employee(
                employee.id, period_start, period_end, session
            )

        print(f"[{datetime.now()}] Расчёт зарплаты завершён")


def start_scheduler():
    scheduler = AsyncIOScheduler()

    # For test - start every 30 sec
    scheduler.add_job(monthly_salary_job, "interval", seconds=30, id="monthly_salary_job")

    # Working one, use for prod
    # scheduler.add_job(monthly_salary_job, "cron", day=1, hour=0, minute=0, id="monthly_salary_job")

    scheduler.start()
    print("Scheduler started!")

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped")


if __name__ == "__main__":
    start_scheduler()
