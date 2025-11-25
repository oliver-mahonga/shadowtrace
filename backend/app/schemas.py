# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class DeviceCreate(BaseModel):
    device_uuid: str
    display_name: str | None = None

class DeviceOut(BaseModel):
    id: str
    device_uuid: str
    display_name: str | None = None
    status: str | None = None
    last_active: datetime | None = None

    class Config:
        orm_mode = True

class LocationPayload(BaseModel):
    lat: float
    lon: float
    accuracy: float | None = None
    speed: float | None = None
    bearing: float | None = None
    recorded_at: datetime | None = None
