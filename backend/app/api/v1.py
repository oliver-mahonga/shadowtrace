# backend/app/api/v1.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from ..db import get_db
from .. import crud, schemas, auth
from pydantic import BaseModel
import redis.asyncio as aioredis
import os
import json

router = APIRouter()

# Redis client (for action queue)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

# --- AUTH ---
class RegisterIn(BaseModel):
    email: str
    password: str

class LoginIn(BaseModel):
    email: str
    password: str

@router.post("/auth/register", response_model=dict)
async def register(payload: RegisterIn, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = auth.hash_password(payload.password)
    user = await crud.create_user(db, payload.email, hashed)
    token = auth.create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/auth/login", response_model=dict)
async def login(payload: LoginIn, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_email(db, payload.email)
    if not user or not auth.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth.create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}

# --- DEVICE REGISTRATION & LIST ---
@router.post("/devices/register", response_model=schemas.DeviceOut)
async def register_device(payload: schemas.DeviceCreate, db: AsyncSession = Depends(get_db)):
    # For now, associate with a dummy user or None — in production require auth
    # Create device
    device = await crud.create_device(db, None, payload.device_uuid, payload.display_name)
    return schemas.DeviceOut.from_orm(device)

@router.get("/devices", response_model=List[schemas.DeviceOut])
async def list_devices(db: AsyncSession = Depends(get_db)):
    # Return all devices (in a real app filter by user)
    res = await db.execute("SELECT id, device_uuid, display_name, status, last_active FROM devices ORDER BY created_at DESC")
    rows = res.fetchall()
    out = []
    for r in rows:
        out.append({
            "id": str(r.id),
            "device_uuid": r.device_uuid,
            "display_name": r.display_name,
            "status": r.status,
            "last_active": r.last_active
        })
    return out

# --- LOCATION ENDPOINTS ---
@router.post("/devices/{device_id}/locations")
async def post_location(device_id: str, payload: schemas.LocationPayload, db: AsyncSession = Depends(get_db)):
    device = await crud.get_device_by_uuid(db, device_id)  # support device_uuid or DB id - adjust as needed
    if not device:
        # try by id
        q = await db.execute("SELECT id FROM devices WHERE id = :id", {"id": device_id})
        if not q.first():
            raise HTTPException(status_code=404, detail="Device not found")
    # Insert
    rec = await crud.add_location(db, device_id, payload.lat, payload.lon, payload.accuracy, payload.speed, payload.bearing, payload.recorded_at)
    return {"ok": True, "location": rec}

@router.get("/devices/{device_id}/last_location")
async def last_location(device_id: str, db: AsyncSession = Depends(get_db)):
    last = await crud.get_last_location(db, device_id)
    return {"location": last}

@router.get("/devices/{device_id}/locations")
async def locations(device_id: str, start: Optional[str] = None, end: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    items = await crud.get_locations(db, device_id, start, end)
    return {"items": items}

@router.get("/devices/{device_id}/trajectory")
async def trajectory(device_id: str, start: Optional[str] = None, end: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    geo = await crud.get_trajectory_geojson(db, device_id, start, end)
    return {"geojson": geo}

# --- GEOFENCE ---
@router.post("/geofences")
async def create_geofence(payload: dict, db: AsyncSession = Depends(get_db)):
    # Accept GeoJSON polygon in payload['geom'] or 'geojson'
    geom = payload.get("geom") or payload.get("geojson")
    name = payload.get("name", "geofence")
    if not geom:
        raise HTTPException(400, "geom required (GeoJSON)")
    # store raw geojson as geom
    stmt = text("INSERT INTO geofences (owner_id, name, geom) VALUES (NULL, :name, ST_SetSRID(ST_GeomFromGeoJSON(:geojson), 4326)) RETURNING id")
    res = await db.execute(stmt, {"name": name, "geojson": json.dumps(geom)})
    new_id = res.scalar_one()
    await db.commit()
    return {"id": str(new_id)}

# --- ACTIONS (REMOTE CONTROL) ---
class ActionIn(BaseModel):
    action: str
    params: Optional[dict] = {}

@router.post("/devices/{device_id}/action")
async def device_action(device_id: str, payload: ActionIn, db: AsyncSession = Depends(get_db)):
    # Log event to events table
    stmt = text("INSERT INTO events (device_id, type, payload) VALUES (:device_id, :type, :payload)")
    await db.execute(stmt, {"device_id": device_id, "type": f"action:{payload.action}", "payload": json.dumps(payload.params)})
    await db.commit()
    # push to redis so agent can pick it up
    queue_key = f"device:{device_id}:actions"
    await redis_client.rpush(queue_key, json.dumps({"action": payload.action, "params": payload.params}))
    return {"status": "queued", "device": device_id, "action": payload.action}
