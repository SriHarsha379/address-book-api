"""Pydantic schemas (request/response models) with validation."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AddressBase(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    latitude: float = Field(..., ge=-90, le=90, description="Latitude (-90 to 90).")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude (-180 to 180).")


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    # Allow partial update; validate ranges when provided
    name: Optional[str] = Field(default=None, max_length=255)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)


class AddressOut(AddressBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
