from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import get_rate
from app.schemas import InsuranceRequest, InsuranceResponse

router = APIRouter()

@router.post("/calculate", response_model=InsuranceResponse)
async def calculate_insurance(request: InsuranceRequest, db: AsyncSession = Depends(get_db)):
    rate = await get_rate(db, cargo_type=request.cargo_type, date=request.date)
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found")
    insurance_cost = request.declared_value * rate.rate
    return {"insurance_cost": insurance_cost}

