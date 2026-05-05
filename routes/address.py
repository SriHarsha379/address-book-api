"""API routes for addresses."""

from __future__ import annotations

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import crud
from database import get_db
from schemas import AddressCreate, AddressOut, AddressUpdate
from utils.distance import haversine_km

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.post("", response_model=AddressOut, status_code=status.HTTP_201_CREATED)
def create_address(payload: AddressCreate, db: Session = Depends(get_db)) -> AddressOut:
    logger.info("Creating address name=%s lat=%s lon=%s", payload.name, payload.latitude, payload.longitude)
    return crud.create_address(db, payload)


@router.get("", response_model=List[AddressOut])
def get_all_addresses(db: Session = Depends(get_db)) -> List[AddressOut]:
    return list(crud.list_addresses(db))


@router.put("/{address_id}", response_model=AddressOut)
def update_address(address_id: int, payload: AddressUpdate, db: Session = Depends(get_db)) -> AddressOut:
    address = crud.get_address(db, address_id)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

    logger.info("Updating address id=%s", address_id)
    return crud.update_address(db, address, payload)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_address(address_id: int, db: Session = Depends(get_db)) -> None:
    address = crud.get_address(db, address_id)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

    logger.info("Deleting address id=%s", address_id)
    crud.delete_address(db, address)
    return None


@router.get("/nearby", response_model=List[AddressOut])
def nearby_addresses(
    lat: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)."),
    lon: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)."),
    distance: float = Query(..., gt=0, description="Search radius in kilometers."),
    db: Session = Depends(get_db),
) -> List[AddressOut]:
    """Return all addresses within the given distance (km) of the provided point."""

    all_addresses = crud.list_addresses(db)
    results = []
    for a in all_addresses:
        d = haversine_km(lat, lon, a.latitude, a.longitude)
        if d <= distance:
            results.append(a)

    logger.info("Nearby search lat=%s lon=%s distance_km=%s results=%s", lat, lon, distance, len(results))
    return list(results)
