# backend/app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from . import models
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping

async def create_user(session: AsyncSession, email: str, hashed_password: str):
    u = models.User(email=email, hashed_password=hashed_password)
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u

async def get_user_by_email(session: AsyncSession, email: str):
    q = await session.execute(select(models.User).where(models.User.email == email))
    return q.scalar_one_or_none()

async def create_device(session: AsyncSession, user_id, device_uuid: str, display_name: str | None = None):
    d = models.Device(user_id=user_id, device_uuid=device_uuid, display_name=display_name)
    session.add(d)
    await session.commit()
    await session.refresh(d)
    return d

async def get_device_by_uuid(session: AsyncSession, device_uuid: str):
    q = await session.execute(select(models.Device).where(models.Device.device_uuid == device_uuid))
    return q.scalar_one_or_none()

async def get_device_by_id(session: AsyncSession, id_):
    q = await session.execute(select(models.Device).where(models.Device.id == id_))
    return q.scalar_one_or_none()

async def list_devices(session: AsyncSession, limit: int = 100):
    q = await session.execute(select(models.Device).order_by(models.Device.created_at.desc()).limit(limit))
    return q.scalars().all()

async def add_location(session: AsyncSession, device_id: str, lat: float, lon: float, accuracy=None, speed=None, bearing=None, recorded_at=None):
    stmt = text(
        "INSERT INTO locations (device_id, recorded_at, geom, accuracy_m, speed, altitude) "
        "VALUES (:device_id, coalesce(:recorded_at, now()), ST_SetSRID(ST_MakePoint(:lon, :lat), 4326), :accuracy, :speed, :bearing) RETURNING id;"
    )
    res = await session.execute(stmt, {"device_id": device_id, "lon": lon, "lat": lat, "accuracy": accuracy, "speed": speed, "bearing": bearing, "recorded_at": recorded_at})
    new_id = res.scalar_one()
    await session.commit()
    q = await session.execute(text("SELECT id, device_id, ST_X(geom) as lon, ST_Y(geom) as lat, accuracy_m, speed, recorded_at FROM locations WHERE id = :id"), {"id": new_id})
    r = q.first()
    return {
        "id": str(r.id),
        "device_id": str(r.device_id),
        "lat": r.lat,
        "lon": r.lon,
        "accuracy": r.accuracy_m,
        "speed": r.speed,
        "recorded_at": r.recorded_at
    }

async def get_last_location(session: AsyncSession, device_id: str):
    q = await session.execute(text("SELECT id, ST_X(geom) as lon, ST_Y(geom) as lat, accuracy_m, speed, recorded_at FROM locations WHERE device_id = :device_id ORDER BY recorded_at DESC LIMIT 1"), {"device_id": device_id})
    r = q.first()
    if not r:
        return None
    return {"id": str(r.id), "lat": r.lat, "lon": r.lon, "accuracy": r.accuracy_m, "speed": r.speed, "recorded_at": r.recorded_at}

async def get_locations_in_range(session: AsyncSession, device_id: str, start: str | None = None, end: str | None = None):
    sql = "SELECT id, ST_X(geom) as lon, ST_Y(geom) as lat, accuracy_m, speed, recorded_at FROM locations WHERE device_id = :device_id"
    params = {"device_id": device_id}
    if start:
        sql += " AND recorded_at >= :start"
        params["start"] = start
    if end:
        sql += " AND recorded_at <= :end"
        params["end"] = end
    sql += " ORDER BY recorded_at ASC"
    q = await session.execute(text(sql), params)
    rows = q.fetchall()
    return [{"id": str(r.id), "lat": r.lat, "lon": r.lon, "accuracy": r.accuracy_m, "speed": r.speed, "recorded_at": r.recorded_at} for r in rows]

async def get_trajectory_geojson(session: AsyncSession, device_id: str, start: str | None = None, end: str | None = None):
    sql = "SELECT ST_AsGeoJSON(ST_MakeLine(geom ORDER BY recorded_at)) as geojson FROM locations WHERE device_id = :device_id"
    params = {"device_id": device_id}
    if start:
        sql += " AND recorded_at >= :start"
        params["start"] = start
    if end:
        sql += " AND recorded_at <= :end"
        params["end"] = end
    q = await session.execute(text(sql), params)
    row = q.first()
    if not row or not row.geojson:
        return None
    import json
    return json.loads(row.geojson)
