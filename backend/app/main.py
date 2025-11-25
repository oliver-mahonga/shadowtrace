# backend/app/main.py
from fastapi import FastAPI
from .api import v1
from .db import engine, Base
import logging

logger = logging.getLogger("uvicorn.error")
app = FastAPI(title="ShadowTrace API")
app.include_router(v1.router)

@app.on_event("startup")
async def startup():
    # create tables (development convenience)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("DB tables ensured")
