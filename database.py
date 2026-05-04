"""Database setup and session management for the application."""

from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DB_PATH = os.getenv("ADDRESS_BOOK_DB_PATH", "address_book.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# check_same_thread=False is required for SQLite usage with FastAPI (multiple threads)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that provides a SQLAlchemy session and ensures it is closed."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
