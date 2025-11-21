from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class RegisterModel(BaseModel):
    username: str
    password: str

class LoginModel(BaseModel):
    username: str
    password: str

class DeviceRegistration(BaseModel):
    device_name: str

class LocationPayload(BaseModel):
    lat: float
    lon: float
    accuracy: float | None = None
    recorded_at: str | None = None
    speed: float | None = None
    altitude: float | None = None


@router.post("/auth/register")
async def register(payload: RegisterModel):
    pass


@router.post("/auth/login")
async def login(payload: LoginModel):
    pass


@router.post("/devices/register")
async def register_device(payload: DeviceRegistration):
    pass


@router.post("/devices/{device_id}/locations")
async def upload_location(device_id: str, payload: LocationPayload):
    """
    Accepts location samples and stores as POINT SRID 4326.
    """
    pass


@router.get("/devices/{device_id}/last_location")
async def last_location(device_id: str):
    pass


@router.get("/devices/{device_id}/trajectory")
async def trajectory(device_id: str, start: str | None = None, end: str | None = None):
    pass


@router.post("/geofences")
async def create_geofence(payload: dict):
    pass


@router.post("/devices/{device_id}/action")
async def remote_action(device_id: str, action: dict):
    pass
