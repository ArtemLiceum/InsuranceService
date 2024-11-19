from fastapi import FastAPI
from app.database import engine, Base, AsyncSessionLocal
from app.routes import router
from app.crud import add_rates

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

    # Add rates to the database
    db = AsyncSessionLocal()  # Create a new session
    try:
        await add_rates(db)  # Add rates asynchronously
    finally:
        await db.close()  # Ensure the session is closed

# Include router for handling routes
app.include_router(router)
