from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Rate
from datetime import datetime

# Получение тарифа
async def get_rate(db: AsyncSession, cargo_type: str, date: datetime):
    query = select(Rate).filter(Rate.cargo_type == cargo_type, Rate.date <= date).order_by(Rate.date.desc())
    result = await db.execute(query)
    return result.scalars().first()

# Добавление тарифов
async def add_rates(db: AsyncSession):
    data = [
        {"date": datetime(2020, 6, 1), "cargo_type": "Glass", "rate": 0.04},
        {"date": datetime(2020, 6, 1), "cargo_type": "Other", "rate": 0.01},
        {"date": datetime(2020, 7, 1), "cargo_type": "Glass", "rate": 0.035},
        {"date": datetime(2020, 7, 1), "cargo_type": "Other", "rate": 0.015},
    ]

    for entry in data:
        rate = Rate(**entry)
        db.add(rate)
    await db.commit()

# Удаление тарифа по критериям
async def delete_rate_by_criteria(db: AsyncSession, cargo_type: str, effective_date: datetime):
    query = select(Rate).where(Rate.cargo_type == cargo_type, Rate.date == effective_date)
    result = await db.execute(query)
    rate = result.scalar_one_or_none()
    if rate:
        await db.delete(rate)
        await db.commit()
    return rate

# Редактирование тарифа
async def update_rate(db: AsyncSession, cargo_type: str, effective_date: datetime, new_data: dict):
    query = await db.execute(
        select(Rate).where(Rate.cargo_type == cargo_type, Rate.date == effective_date)
    )
    rate = query.scalar_one_or_none()

    if not rate:
        return None

    # Обновление данных
    for key, value in new_data.items():
        if hasattr(rate, key):
            setattr(rate, key, value)

    await db.commit()
    await db.refresh(rate)
    return rate
