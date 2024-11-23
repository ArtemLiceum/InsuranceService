from fastapi import FastAPI
from app.database import engine, Base, AsyncSessionLocal
from app.routes import router
from app.crud import add_rates, init_kafka, close_kafka

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        await add_rates(db)

    # Инициализация Kafka
    await init_kafka()


@app.on_event("shutdown")
async def shutdown_event():
    await close_kafka()


app.include_router(router)
