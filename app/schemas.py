from pydantic import BaseModel
from datetime import date

class RateCreate(BaseModel):
    date: date
    cargo_type: str
    rate: float

class InsuranceRequest(BaseModel):
    cargo_type: str
    declared_value: float
    date: date

class InsuranceResponse(BaseModel):
    insurance_cost: float

class RateUpdate(BaseModel):
    rate: float