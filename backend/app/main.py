# backend/app/main.py
from fastapi import FastAPI
from .api import v1
from .api import ws
from .db import engine, Base
import logging
import sqlalchemy
import os

logger = logging.getLogger("uvicorn.error")
app = FastAPI(title="ShadowTrace API")

app.include_router(v1.router)
app.include_router(ws.router)

@app.on_event("startup")
async def startup():
    # ensure Postgres extensions and create tables
    async with engine.begin() as conn:
        # enable pgcrypto for gen_random_uuid
        try:
            await conn.execute(sqlalchemy.text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
        except Exception as e:
            logger.warning("Could not create pgcrypto extension: %s", e)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("DB tables ensured and extensions installed (if possible)")
