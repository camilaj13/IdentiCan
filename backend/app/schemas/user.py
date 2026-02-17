from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.schemas.dog import DogResponse


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    phone: Optional[str] = None
    role: str
    is_premium: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserWithDogsResponse(BaseModel):
    id: int
    email: str
    name: str
    phone: Optional[str] = None
    role: str
    is_premium: bool
    created_at: datetime
    dogs: List[DogResponse] = []

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
