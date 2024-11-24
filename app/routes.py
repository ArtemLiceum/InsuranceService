from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.database import get_db
from app.crud import get_rate, delete_rate_by_criteria, update_rate
from app.schemas import InsuranceRequest, InsuranceResponse, RateUpdate
from app.kafka_logger import log_action
import traceback

router = APIRouter()

@router.post("/calculate", response_model=InsuranceResponse)
async def calculate_insurance(request: InsuranceRequest, db: AsyncSession = Depends(get_db)):
    try:
        rate = await get_rate(db, cargo_type=request.cargo_type, date=request.date)
        if not rate:
            raise HTTPException(status_code=404, detail="Rate not found")
        insurance_cost = request.declared_value * rate.rate
        return {"insurance_cost": insurance_cost}
    except Exception as e:
        log_action("error", {"endpoint": "/calculate", "error": repr(e), "traceback": traceback.format_exc()})
        raise HTTPException(status_code=500, detail="An internal error occurred.")

@router.delete("/rates/{cargo_type}/{effective_date}", response_model=dict)
async def delete_rate_endpoint(cargo_type: str, effective_date: str, db: AsyncSession = Depends(get_db)):
    try:
        effective_date_parsed = datetime.strptime(effective_date, "%Y-%m-%d")
        rate = await delete_rate_by_criteria(db, cargo_type, effective_date_parsed)
        if not rate:
            raise HTTPException(status_code=404, detail="Rate not found")
        return {"message": "Rate deleted successfully"}
    except Exception as e:
        log_action("error", {"endpoint": "/rates/delete", "error": repr(e), "traceback": traceback.format_exc()})
        raise HTTPException(status_code=500, detail="An internal error occurred.")

@router.put("/rates/{cargo_type}/{effective_date}", response_model=dict)
async def update_rate_endpoint(cargo_type: str, effective_date: str, rate_data: RateUpdate, db: AsyncSession = Depends(get_db)):
    try:
        effective_date_parsed = datetime.strptime(effective_date, "%Y-%m-%d")
        updated_rate = await update_rate(db, cargo_type, effective_date_parsed, rate_data.dict(exclude_unset=True))
        if not updated_rate:
            raise HTTPException(status_code=404, detail="Rate not found")
        return {"message": "Rate updated successfully"}
    except Exception as e:
        log_action("error", {"endpoint": "/rates/update", "error": repr(e), "traceback": traceback.format_exc()})
        raise HTTPException(status_code=500, detail="An internal error occurred.")
