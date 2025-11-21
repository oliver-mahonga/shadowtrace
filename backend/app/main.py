# backend/app/main.py
from fastapi import FastAPI
from app.api import v1
app = FastAPI(title="ShadowTrace API")

app.include_router(v1.router, prefix="/api/v1")
