# backend/app/models.py
from sqlalchemy import Column, String, DateTime, JSON, Float, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from .db import Base
import datetime
import uuid
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Device(Base):
    __tablename__ = "devices"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    device_uuid = Column(String, unique=True, nullable=False)
    display_name = Column(String)
    public_key = Column(String)
    status = Column(String, default="active")
    last_active = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

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
    metadata = Column(JSON, default={})
