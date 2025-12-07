# backend/app/api/v1.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from ..db import get_db
from .. import crud, schemas, auth
from pydantic import BaseModel
import redis.asyncio as aioredis
import os
import json

router = APIRouter(prefix="/api/v1")
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
    device = await crud.create_device(db, None, payload.device_uuid, payload.display_name)
    return schemas.DeviceOut.from_orm(device)

@router.get("/devices", response_model=List[schemas.DeviceOut])
async def list_devices(db: AsyncSession = Depends(get_db)):
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
    # Support device_uuid or DB id
    device = await crud.get_device_by_uuid(db, device_id)
    if not device:
        q = await db.execute("SELECT id FROM devices WHERE id = :id", {"id": device_id})
        if not q.first():
            raise HTTPException(status_code=404, detail="Device not found")
    rec = await crud.add_location(db, device_id, payload.lat, payload.lon, payload.accuracy, payload.speed, payload.bearing, payload.recorded_at)
    # update last_active
    await db.execute("UPDATE devices SET last_active = now() WHERE device_uuid = :uuid OR id = :id", {"uuid": device_id, "id": device_id})
    await db.commit()
    # optionally push to redis/pubsub for realtime consumers
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

# --- ACTIONS (REMOTE CONTROL) ---
class ActionIn(BaseModel):
    action: str
    params: Optional[dict] = {}

@router.post("/devices/{device_id}/action")
async def device_action(device_id: str, payload: ActionIn, db: AsyncSession = Depends(get_db)):
    # Insert command record
    cmd = await crud.create_device_command(db, device_id, payload.action, payload.params)
    # push to redis queue for device to pick up
    queue_key = f"device:{device_id}:actions"
    await redis_client.rpush(queue_key, json.dumps({"command_id": cmd["id"], "action": payload.action, "params": payload.params}))
    return {"status": "queued", "device": device_id, "action": payload.action, "command_id": cmd["id"]}

@router.get("/devices/{device_id}/actions/next")
async def poll_actions(device_id: str):
    queue_key = f"device:{device_id}:actions"
    data = await redis_client.lpop(queue_key)
    if not data:
        return {"action": None}
    return {"action": json.loads(data)}

# Device posts command response (file uploads or JSON)
@router.post("/devices/{device_id}/action/{command_id}/response")
async def action_response(device_id: str, command_id: str, response_type: str = "ack", file: Optional[UploadFile] = File(None), db: AsyncSession = Depends(get_db)):
    payload = {}
    if file:
        contents = await file.read()
        path = f"uploads/{device_id}_{command_id}_{file.filename}"
        with open(path, "wb") as f:
            f.write(contents)
        payload["file_path"] = path
        payload["media_type"] = file.content_type
    # insert response
    stmt = "INSERT INTO device_responses (command_id, response_type, payload) VALUES (:command_id, :response_type, :payload)"
    await db.execute(text(stmt), {"command_id": command_id, "response_type": response_type, "payload": json.dumps(payload)})
    await crud.mark_command_executed(db, command_id)
    return {"ok": True}

# --- EVIDENCE UPLOAD ---
@router.post("/devices/{device_id}/evidence")
async def upload_evidence(device_id: str, file: UploadFile = File(...), recorded_at: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    contents = await file.read()
    path = f"uploads/{device_id}_{file.filename}"
    with open(path, "wb") as f:
        f.write(contents)
    stmt = "INSERT INTO evidence (device_id, recorded_at, media_type, s3_path) VALUES (:device_id, coalesce(:recorded_at, now()), :media_type, :path)"
    await db.execute(text(stmt), {"device_id": device_id, "recorded_at": recorded_at, "media_type": file.content_type, "path": path})
    await db.commit()
    return {"status": "stored", "path": path}
