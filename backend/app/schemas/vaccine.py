from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class VaccineCreate(BaseModel):
    dog_id: int
    vaccine_type: str = Field(..., min_length=1, max_length=100)
    vaccine_date: date
    next_dose_date: Optional[date] = None
    veterinarian_name: Optional[str] = None
    clinic_name: Optional[str] = None
    batch_number: Optional[str] = None
    certificate_url: Optional[str] = None
    notes: Optional[str] = None


class VaccineResponse(BaseModel):
    id: int
    dog_id: int
    vaccine_type: str
    vaccine_date: date
    next_dose_date: Optional[date] = None
    veterinarian_name: Optional[str] = None
    clinic_name: Optional[str] = None
    batch_number: Optional[str] = None
    certificate_url: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
