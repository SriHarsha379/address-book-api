"""
FastAPI application entry point.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI

from database import Base, engine
from routes.address import router as address_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

app = FastAPI(
    title="Address Book API",
    version="1.0.0",
)

# Create tables on startup (simple/minimal approach for SQLite apps)
Base.metadata.create_all(bind=engine)

app.include_router(address_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
