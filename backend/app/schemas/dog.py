from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class DogCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    breed: Optional[str] = None
    birth_date: Optional[date] = None
    age_years: Optional[int] = Field(None, ge=0, le=30)
    weight_kg: Optional[float] = Field(None, ge=0, le=150)
    sex: str = Field(..., pattern=r"^[MF]$")
    color: Optional[str] = None
    origin: str = Field(..., pattern=r"^(adopted|purchased|rescued|other)$")
    microchip_id: Optional[str] = None
    behavior_notes: Optional[str] = None
    likes: Optional[str] = None
    allergies: Optional[str] = None
    from_shelter: bool = False
    shelter_name: Optional[str] = None
    previous_owner_name: Optional[str] = None


class DogUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    breed: Optional[str] = None
    birth_date: Optional[date] = None
    age_years: Optional[int] = Field(None, ge=0, le=30)
    weight_kg: Optional[float] = Field(None, ge=0, le=150)
    sex: Optional[str] = Field(None, pattern=r"^[MF]$")
    color: Optional[str] = None
    origin: Optional[str] = Field(None, pattern=r"^(adopted|purchased|rescued|other)$")
    microchip_id: Optional[str] = None
    behavior_notes: Optional[str] = None
    likes: Optional[str] = None
    allergies: Optional[str] = None
    from_shelter: Optional[bool] = None
    shelter_name: Optional[str] = None
    previous_owner_name: Optional[str] = None


class DogResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    breed: Optional[str] = None
    birth_date: Optional[date] = None
    age_years: Optional[int] = None
    weight_kg: Optional[float] = None
    sex: str
    color: Optional[str] = None
    origin: str
    nose_images: List[str] = []
    qr_code: str
    microchip_id: Optional[str] = None
    behavior_notes: Optional[str] = None
    likes: Optional[str] = None
    allergies: Optional[str] = None
    from_shelter: bool
    shelter_name: Optional[str] = None
    previous_owner_name: Optional[str] = None
    health_booklet_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
