from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Rate
from datetime import datetime
from aiokafka import AIOKafkaProducer

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

# Удаление тарифа
async def delete_rate(db: AsyncSession, rate_id: int):
    rate = await db.get(Rate, rate_id)
    if rate:
        await db.delete(rate)
        await db.commit()
    return rate

# Редактирование тарифа
async def update_rate(db: AsyncSession, rate_id: int, new_data: dict):
    rate = await db.get(Rate, rate_id)
    if rate:
        for key, value in new_data.items():
            setattr(rate, key, value)
        await db.commit()
    return rate

# Kafka producer
kafka_producer = None

async def init_kafka():
    global kafka_producer
    kafka_producer = AIOKafkaProducer(bootstrap_servers="kafka:29092")
    await kafka_producer.start()

async def close_kafka():
    global kafka_producer
    if kafka_producer:
        await kafka_producer.stop()
