# backend/app/schemas.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
import uuid

# --- User/Auth Schemas ---

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserRegister(UserBase):
    password: str = Field(..., min_length=8)
    confirm_password: str # Field for password confirmation

    @validator('confirm_password', always=True)
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match.')
        return v

class UserLogin(BaseModel):
    username: str # Login via username
    password: str

class UserOut(UserBase):
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Device Schemas ---

class DeviceCreate(BaseModel):
    # Renamed from device_uuid to unique_device_id for consistency
    unique_device_id: str = Field(..., max_length=255)
    display_name: str | None = None

class DeviceOut(BaseModel):
    id: uuid.UUID
    unique_device_id: str
    display_name: str | None = None
    status: str | None = None
    last_active: datetime | None = None

    class Config:
        from_attributes = True

# --- Location Schemas (Input/Output) ---
class LocationPayload(BaseModel):
    lat: float
    lon: float
    accuracy: float | None = None
    speed: float | None = None
    bearing: float | None = None
    recorded_at: datetime | None = None

class LocationOut(BaseModel):
    id: uuid.UUID
    device_id: uuid.UUID
    lat: float
    lon: float
    accuracy: float | None = None
    speed: float | None = None
    recorded_at: datetime

    class Config:
        from_attributes = True

# --- Command/Action Schemas (Remote Control) ---
class CommandCreate(BaseModel):
    action: str = Field(..., description="e.g., 'LOCK', 'SOUND_SIREN', 'GET_IMAGE'")
    params: Optional[dict] = {}

class CommandOut(BaseModel):
    id: uuid.UUID
    device_id: uuid.UUID
    type: str # The action type
    payload: dict
    status: str
    occurred_at: datetime

    class Config:
        from_attributes = True

class CommandStatusUpdate(BaseModel):
    command_id: uuid.UUID
    status: str = Field(..., description="e.g., 'EXECUTED', 'FAILED', 'ACKNOWLEDGED'")
    payload: Optional[dict] = {} # For results, like an S3 path to an image
    
# --- Geofence Input Schema ---
class GeofenceIn(BaseModel):
    name: str
    # GeoJSON Polygon structure is complex, use dict for simplicity here
    geojson: dict # Must be a GeoJSON Polygon Geometry or Feature