# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class DeviceCreate(BaseModel):
    device_uuid: str
    display_name: Optional[str] = None

class DeviceOut(BaseModel):
    id: str
    device_uuid: str
    display_name: Optional[str] = None
    status: Optional[str] = None
    last_active: Optional[datetime] = None

    class Config:
        orm_mode = True

class LocationPayload(BaseModel):
    lat: float
    lon: float
    accuracy: Optional[float] = None
    speed: Optional[float] = None
    bearing: Optional[float] = None
    recorded_at: Optional[datetime] = None

class ActionIn(BaseModel):
    action: str
    params: Optional[dict] = {}
