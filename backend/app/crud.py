# backend/app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from . import models, schemas
from datetime import datetime
import uuid
import json

# --- User CRUD ---
async def create_user(session: AsyncSession, user: schemas.UserRegister, hashed_password: str):
    u = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u

async def get_user_by_email(session: AsyncSession, email: str):
    q = await session.execute(select(models.User).where(models.User.email == email))
    return q.scalar_one_or_none()

async def get_user_by_username(session: AsyncSession, username: str):
    q = await session.execute(select(models.User).where(models.User.username == username))
    return q.scalar_one_or_none()

# --- Device CRUD ---
async def create_device(session: AsyncSession, user_id: uuid.UUID, unique_device_id: str, display_name: str | None = None):
    d = models.Device(user_id=user_id, unique_device_id=unique_device_id, display_name=display_name)
    session.add(d)
    await session.commit()
    await session.refresh(d)
    return d

async def get_device_by_unique_id(session: AsyncSession, unique_device_id: str):
    q = await session.execute(select(models.Device).where(models.Device.unique_device_id == unique_device_id))
    return q.scalar_one_or_none()

async def get_device_by_id(session: AsyncSession, id_: uuid.UUID):
    q = await session.execute(select(models.Device).where(models.Device.id == id_))
    return q.scalar_one_or_none()
    
async def get_device_by_id_and_owner(session: AsyncSession, device_id: uuid.UUID, user_id: uuid.UUID):
    q = await session.execute(select(models.Device).where(
        models.Device.id == device_id,
        models.Device.user_id == user_id
    ))
    return q.scalar_one_or_none()

async def list_devices_by_user(session: AsyncSession, user_id: uuid.UUID):
    q = await session.execute(select(models.Device).where(models.Device.user_id == user_id).order_by(models.Device.created_at.desc()))
    return q.scalars().all()
    
# --- Location CRUD ---
async def add_location(session: AsyncSession, device_id: uuid.UUID, lat: float, lon: float, accuracy=None, speed=None, bearing=None, recorded_at=None):
    
    # 1. Update device's last active time
    await session.execute(
        text("UPDATE devices SET last_active = :now WHERE id = :device_id"), 
        {"now": datetime.utcnow(), "device_id": device_id}
    )
    
    # 2. Insert new location record
    l = models.Location(
        device_id=device_id,
        recorded_at=recorded_at if recorded_at else datetime.utcnow(),
        geom=f'POINT({lon} {lat})', 
        accuracy_m=accuracy,
        speed=speed
    )
    session.add(l)
    await session.commit()
    await session.refresh(l)

    # 3. Return a consistent dictionary structure
    return {
        "id": str(l.id),
        "device_id": str(l.device_id),
        "lat": lat,
        "lon": lon,
        "accuracy": l.accuracy_m,
        "speed": l.speed,
        "recorded_at": l.recorded_at
    }

async def get_last_location(session: AsyncSession, device_id: uuid.UUID):
    q = await session.execute(text("SELECT id, ST_X(geom) as lon, ST_Y(geom) as lat, accuracy_m, speed, recorded_at FROM locations WHERE device_id = :device_id ORDER BY recorded_at DESC LIMIT 1"), {"device_id": device_id})
    r = q.first()
    if not r:
        return None
    return {"id": str(r.id), "lat": r.lat, "lon": r.lon, "accuracy": r.accuracy_m, "speed": r.speed, "recorded_at": r.recorded_at}

# --- Location History and Trajectory Retrieval ---
async def get_locations_in_range(session: AsyncSession, device_id: uuid.UUID, start: str | None = None, end: str | None = None):
    """Retrieves all location points for a device in a given time range."""
    sql = "SELECT id, ST_X(geom) as lon, ST_Y(geom) as lat, accuracy_m, speed, recorded_at FROM locations WHERE device_id = :device_id"
    params = {"device_id": str(device_id)}
    if start:
        sql += " AND recorded_at >= :start"
        params["start"] = start
    if end:
        sql += " AND recorded_at <= :end"
        params["end"] = end
    sql += " ORDER BY recorded_at ASC"
    
    q = await session.execute(text(sql), params)
    rows = q.fetchall()
    return [{
        "id": str(r.id), 
        "lat": r.lat, 
        "lon": r.lon, 
        "accuracy": r.accuracy_m, 
        "speed": r.speed, 
        "recorded_at": r.recorded_at
    } for r in rows]

async def get_trajectory_geojson(session: AsyncSession, device_id: uuid.UUID, start: str | None = None, end: str | None = None):
    """Computes a GeoJSON LineString representing the device's path."""
    sql = "SELECT ST_AsGeoJSON(ST_MakeLine(geom ORDER BY recorded_at)) as geojson FROM locations WHERE device_id = :device_id"
    params = {"device_id": str(device_id)}
    if start:
        sql += " AND recorded_at >= :start"
        params["start"] = start
    if end:
        sql += " AND recorded_at <= :end"
        params["end"] = end
        
    q = await session.execute(text(sql), params)
    row = q.first()
    
    if not row or not row.geojson:
        # Return a valid empty GeoJSON FeatureCollection if no line is formed
        return {"type": "FeatureCollection", "features": []}
    
    line_feature = {
        "type": "Feature",
        "geometry": json.loads(row.geojson),
        "properties": {"device_id": str(device_id)}
    }
    return {"type": "FeatureCollection", "features": [line_feature]}


# --- Geofence CRUD ---
async def create_geofence(session: AsyncSession, owner_id: uuid.UUID, name: str, geojson_polygon: dict) -> uuid.UUID:
    """Inserts a new geofence using a GeoJSON Polygon."""
    stmt = text(
        "INSERT INTO geofences (owner_id, name, geom) "
        "VALUES (:owner_id, :name, ST_SetSRID(ST_GeomFromGeoJSON(:geojson), 4326)) RETURNING id"
    )
    res = await session.execute(stmt, {
        "owner_id": str(owner_id), 
        "name": name, 
        "geojson": json.dumps(geojson_polygon)
    })
    new_id = res.scalar_one()
    await session.commit()
    return new_id

async def list_geofences_by_user(session: AsyncSession, owner_id: uuid.UUID):
    """Retrieves all geofences owned by the user."""
    q = await session.execute(select(models.Geofence).where(models.Geofence.owner_id == owner_id))
    return q.scalars().all()


# --- Command/Action CRUD ---
async def log_command(session: AsyncSession, device_id: uuid.UUID, action: str, params: dict) -> models.CommandLog:
    """Logs the command into the events table with PENDING status."""
    payload = {"action": action, "params": params, "status": "PENDING"}
    command_log = models.CommandLog(device_id=device_id, type=f"action:{action}", payload=payload)
    session.add(command_log)
    await session.commit()
    await session.refresh(command_log)
    return command_log

async def update_command_log_status(session: AsyncSession, command_id: uuid.UUID, status: str, result_payload: dict | None = None):
    """Updates the status of a command based on mobile device feedback."""
    q = await session.execute(select(models.CommandLog).where(models.CommandLog.id == command_id))
    log_entry = q.scalar_one_or_none()
    
    if log_entry:
        current_payload = dict(log_entry.payload)
        current_payload["status"] = status
        if result_payload:
            current_payload.update(result_payload)
            
        log_entry.payload = current_payload
        log_entry.occurred_at = datetime.utcnow()
        await session.commit()
        await session.refresh(log_entry)
        return log_entry
    return None