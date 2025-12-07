# backend/app/models.py
from sqlalchemy import Column, String, DateTime, JSON, Float, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship 
from geoalchemy2 import Geometry
from .db import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False) # ADDED: Username field
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    devices = relationship("Device", back_populates="user") 


class Device(Base):
    __tablename__ = "devices"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    # UPDATED: Renamed from device_uuid to unique_device_id
    unique_device_id = Column(String, unique=True, nullable=False) 
    display_name = Column(String)
    public_key = Column(String)
    status = Column(String, default="active")
    last_active = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="devices") 


class Location(Base):
    __tablename__ = "locations"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"))
    recorded_at = Column(DateTime(timezone=True), nullable=False)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))
    accuracy_m = Column(Float)
    provider = Column(String)
    speed = Column(Float)
    altitude = Column(Float)
    meta = Column(JSON, name="metadata", default={})


class Geofence(Base):
    __tablename__ = "geofences"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(String)
    geom = Column(Geometry(geometry_type='POLYGON', srid=4326))
    action_on_enter = Column(JSON, default={})
    action_on_exit = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Evidence(Base):
    __tablename__ = "evidence"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"))
    recorded_at = Column(DateTime(timezone=True), nullable=False)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))
    s3_path = Column(String)
    media_type = Column(String)
    hash_sha256 = Column(String)
    signed_by_server = Column(String)
    meta = Column(JSON, name="metadata", default={})

# Reusing the 'events' table for Command Logs
class CommandLog(Base):
    __tablename__ = "events" 
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"))
    type = Column(String, nullable=False) # The action (e.g., LOCK)
    payload = Column(JSON, default={}) # Stores command params and status
    occurred_at = Column(DateTime(timezone=True), server_default=func.now())