#backend/models.py
from pydantic import BaseModel,Field
from typing import Optional

class Location(BaseModel):
    lat: float
    lon: float

class PlanRequest(BaseModel):
    origin: Location
    destination: Location
    
class PaymentRequest(BaseModel):
    trip_id: str              = Field(..., example="TEST123")
    amount: float             = Field(..., example=0.0)
    token: Optional[str] = Field(None, example=None)