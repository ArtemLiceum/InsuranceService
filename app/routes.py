from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.database import get_db
from app.crud import get_rate
from app.schemas import InsuranceRequest, InsuranceResponse, RateUpdate
from app.crud import delete_rate, update_rate


router = APIRouter()

@router.post("/calculate", response_model=InsuranceResponse)
async def calculate_insurance(request: InsuranceRequest, db: AsyncSession = Depends(get_db)):
    rate = await get_rate(db, cargo_type=request.cargo_type, date=request.date)
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found")
    insurance_cost = request.declared_value * rate.rate
    return {"insurance_cost": insurance_cost}

@router.delete("/rates/{cargo_type}/{effective_date}", response_model=dict)
async def delete_rate_endpoint(cargo_type: str, effective_date: str, db: AsyncSession = Depends(get_db)):
    try:
        effective_date_parsed = datetime.strptime(effective_date, "%Y-%m-%d")
        success = await delete_rate(db, cargo_type, effective_date_parsed)
        if not success:
            raise HTTPException(status_code=404, detail="Rate not found")
        return {"message": "Rate deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/rates/{cargo_type}/{effective_date}", response_model=dict)
async def update_rate_endpoint(
    cargo_type: str,
    effective_date: str,
    rate_data: RateUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        effective_date_parsed = datetime.strptime(effective_date, "%Y-%m-%d")
        success = await update_rate(db, cargo_type, effective_date_parsed, rate_data)
        if not success:
            raise HTTPException(status_code=404, detail="Rate not found")
        return {"message": "Rate updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
