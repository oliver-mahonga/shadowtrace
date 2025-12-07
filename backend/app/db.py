# backend/app/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from pydantic import BaseSettings
from typing import AsyncGenerator

# Using a Pydantic BaseSettings class for clean configuration loading
class Settings(BaseSettings):
    # This setting must match your docker-compose service setup (postgresql+asyncpg)
    DATABASE_URL: str = "postgresql+asyncpg://st_user:st_pass@localhost:5432/shadowtrace"

settings = Settings()

DATABASE_URL = settings.DATABASE_URL

# --- Engine Setup ---
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# --- Dependency Injection for Routers ---
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()