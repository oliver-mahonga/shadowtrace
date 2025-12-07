# backend/app/api/v1.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Annotated
from ..db import get_db
from .. import crud, schemas, auth, models
import json
import uuid
from .ws import manager 

router = APIRouter(prefix="/v1")

# --- AUTH ---

@router.post("/auth/register", response_model=dict, tags=["1. Authentication"])
async def register(payload: schemas.UserRegister, db: Annotated[AsyncSession, Depends(get_db)]):
    if await crud.get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if await crud.get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Username already taken")
        
    hashed = auth.hash_password(payload.password)
    user = await crud.create_user(db, payload, hashed)
    
    token = auth.create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer", "user_id": str(user.id)}

@router.post("/auth/login", response_model=dict, tags=["1. Authentication"])
async def login(payload: schemas.UserLogin, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await crud.get_user_by_username(db, payload.username)
    
    if not user or not auth.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
    token = auth.create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer", "user_id": str(user.id)}

@router.get("/auth/me", response_model=schemas.UserOut, tags=["1. Authentication"])
async def read_users_me(current_user: Annotated[models.User, Depends(auth.get_current_user)]):
    return current_user

# --- DEVICE MANAGEMENT (SECURED) ---
device_router = APIRouter(prefix="/devices", tags=["2. Device Management"], dependencies=[Depends(auth.get_current_user)])

@device_router.post("/register", response_model=schemas.DeviceOut)
async def register_device(
    payload: schemas.DeviceCreate, 
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    unique_device_id = payload.unique_device_id
    existing = await crud.get_device_by_unique_id(db, unique_device_id)
    if existing:
         raise HTTPException(status_code=400, detail="Device with this ID is already registered.")

    device = await crud.create_device(db, current_user.id, unique_device_id, payload.display_name)
    return schemas.DeviceOut.model_validate(device)

@device_router.get("/", response_model=List[schemas.DeviceOut])
async def list_devices(
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    devices = await crud.list_devices_by_user(db, current_user.id)
    return [schemas.DeviceOut.model_validate(d) for d in devices]

# --- LOCATION REPORTING (DEVICE-ONLY) ---

@router.post("/device_report/location", tags=["Device-Only Reporting"])
async def post_device_location(payload: schemas.LocationPayload, unique_device_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    device = await crud.get_device_by_unique_id(db, unique_device_id)
    if not device:
        raise HTTPException(status_code=403, detail="Device not recognized.")
        
    rec = await crud.add_location(db, device.id, payload.lat, payload.lon, payload.accuracy, payload.speed, payload.bearing, payload.recorded_at)
    return {"ok": True, "location": rec}


# --- LOCATION VIEWING (SECURED) ---
location_router = APIRouter(prefix="/locations", tags=["3. Tracking & Location"], dependencies=[Depends(auth.get_current_user)])

async def check_device_ownership(db: AsyncSession, device_id: uuid.UUID, current_user: models.User):
    device = await crud.get_device_by_id_and_owner(db, device_id, current_user.id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found or unauthorized.")
    return device

@location_router.get("/{device_id}/last", response_model=dict)
async def last_location(
    device_id: uuid.UUID, 
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    await check_device_ownership(db, device_id, current_user)
    last = await crud.get_last_location(db, device_id)
    if not last:
        return {"location": None, "message": "No location history found."}
    
    return {"location": last}

# CORRECTED: Location History Endpoint (Required args first)
@location_router.get("/{device_id}/history", response_model=dict)
async def location_history(
    device_id: uuid.UUID, 
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    start: Optional[str] = None, 
    end: Optional[str] = None, 
):
    await check_device_ownership(db, device_id, current_user)
    items = await crud.get_locations_in_range(db, device_id, start, end)
    return {"items": items}

# CORRECTED: Trajectory GeoJSON Endpoint (Required args first)
@location_router.get("/{device_id}/trajectory", response_model=dict)
async def trajectory(
    device_id: uuid.UUID, 
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    start: Optional[str] = None, 
    end: Optional[str] = None, 
):
    await check_device_ownership(db, device_id, current_user)
    geo = await crud.get_trajectory_geojson(db, device_id, start, end)
    return {"geojson": geo}


# --- GEOFENCE MANAGEMENT (SECURED) ---
geofence_router = APIRouter(prefix="/geofences", tags=["5. Geofencing"], dependencies=[Depends(auth.get_current_user)])


@geofence_router.post("/", response_model=dict)
async def create_geofence(
    payload: schemas.GeofenceIn, 
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Basic GeoJSON validation
    if payload.geojson.get("type") not in ["Polygon", "Feature"]:
         raise HTTPException(400, "GeoJSON must be a Polygon Geometry or Feature containing a Polygon.")
         
    # Extract the geometry dictionary if it's a Feature
    geom_data = payload.geojson.get("geometry", payload.geojson)
    
    new_id = await crud.create_geofence(db, current_user.id, payload.name, geom_data)
    return {"id": str(new_id), "name": payload.name}


# --- ACTIONS (REMOTE CONTROL - SECURED) ---
action_router = APIRouter(prefix="/actions", tags=["4. Remote Control"], dependencies=[Depends(auth.get_current_user)])

@action_router.post("/{device_id}")
async def send_device_action(
    device_id: uuid.UUID, 
    payload: schemas.CommandCreate, 
    current_user: Annotated[models.User, Depends(auth.get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # 1. Check ownership and retrieve device details
    device = await check_device_ownership(db, device_id, current_user)
        
    # 2. Log event/command into the database (PENDING status)
    command_log = await crud.log_command(db, device_id, payload.action, payload.params)
    
    # 3. Prepare the command for the device
    command_data = {
        "command_id": str(command_log.id),
        "action": payload.action,
        "params": payload.params
    }
    command_json = json.dumps(command_data)
    
    # 4. Attempt real-time delivery via WebSocket, otherwise queue in Redis
    is_sent = await manager.send_command_to_device(device.unique_device_id, command_json)
    
    return {
        "status": "SENT" if is_sent else "QUEUED", 
        "command_id": str(command_log.id), 
        "device": str(device_id), 
        "action": payload.action
    }

# --- Register all sub-routers to the V1 Router ---
router.include_router(device_router)
router.include_router(location_router)
router.include_router(action_router)
router.include_router(geofence_router)