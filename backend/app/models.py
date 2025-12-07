# backend/app/models.py
from sqlalchemy import Column, String, DateTime, JSON, Float, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from .db import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Device(Base):
    __tablename__ = "devices"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    device_uuid = Column(String, unique=True, nullable=False)
    display_name = Column(String)
    public_key = Column(String)
    status = Column(String, default="active")
    last_active = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    fcm_token = Column(String, nullable=True)
    device_token = Column(String, nullable=True)

class Location(Base):
    __tablename__ = "locations"
    __table_args__ = {'extend_existing': True}  # <-- fixes duplicate table error

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"))
    recorded_at = Column(DateTime(timezone=True), nullable=False)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))
    accuracy_m = Column(Float)
    provider = Column(String)
    speed = Column(Float)
    altitude = Column(Float)
    extra = Column("metadata", JSON, default=dict)

class Geofence(Base):
    __tablename__ = "geofences"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(String)
    geom = Column(Geometry(geometry_type='POLYGON', srid=4326))
    action_on_enter = Column(JSON, default={})
    action_on_exit = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Event(Base):
    __tablename__ = "events"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"))
    type = Column(String, nullable=False)
    payload = Column(JSON, default={})
    occurred_at = Column(DateTime(timezone=True), server_default=func.now())

class DeviceCommand(Base):
    __tablename__ = "device_commands"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"))
    command_type = Column(String, nullable=False)
    payload = Column(JSON, default={})
    status = Column(String, default="pending")  # pending, sent, executed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class DeviceResponse(Base):
    __tablename__ = "device_responses"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    command_id = Column(UUID(as_uuid=True), ForeignKey("device_commands.id"))
    response_type = Column(String)
    payload = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
