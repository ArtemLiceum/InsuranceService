from fastapi import FastAPI
from app.database import engine, Base, AsyncSessionLocal
from app.routes import router
from app.crud import add_rates

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = AsyncSessionLocal()
    try:
        await add_rates(db)
    finally:
        await db.close()

app.include_router(router)
