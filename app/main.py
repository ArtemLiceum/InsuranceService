from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import engine, Base, AsyncSessionLocal
from app.routes import router
from app.crud import add_rates
from app.kafka_logger import log_action
import traceback

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        await add_rates(db)

@app.on_event("shutdown")
async def shutdown_event():
    pass

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_details = {
        "method": request.method,
        "url": str(request.url),
        "error": repr(exc),
        "traceback": traceback.format_exc()
    }
    log_action("error", error_details)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again later."}
    )

app.include_router(router)
