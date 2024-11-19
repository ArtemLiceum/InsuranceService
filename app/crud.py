from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Rate
from datetime import datetime

async def get_rate(db: AsyncSession, cargo_type: str, date: str):
    query = select(Rate).filter(Rate.cargo_type == cargo_type, Rate.date <= date).order_by(Rate.date.desc())
    result = await db.execute(query)
    return result.scalars().first()


async def add_rates(db: AsyncSession):
    data = [
        {"date": "2020-06-01", "cargo_type": "Glass", "rate": 0.04},
        {"date": "2020-06-01", "cargo_type": "Other", "rate": 0.01},
        {"date": "2020-07-01", "cargo_type": "Glass", "rate": 0.035},
        {"date": "2020-07-01", "cargo_type": "Other", "rate": 0.015},
    ]

    for entry in data:
        entry["date"] = datetime.strptime(entry["date"], "%Y-%m-%d")

    for entry in data:
        rate = Rate(**entry)
        db.add(rate)
    await db.commit()