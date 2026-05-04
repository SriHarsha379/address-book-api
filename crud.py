"""CRUD operations for Address entities."""

from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Address
from schemas import AddressCreate, AddressUpdate


def create_address(db: Session, payload: AddressCreate) -> Address:
    address = Address(
        name=payload.name,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def get_address(db: Session, address_id: int) -> Optional[Address]:
    return db.get(Address, address_id)


def list_addresses(db: Session) -> Sequence[Address]:
    stmt = select(Address).order_by(Address.id.asc())
    return list(db.scalars(stmt).all())


def update_address(db: Session, address: Address, payload: AddressUpdate) -> Address:
    data = payload.model_dump(exclude_unset=True)

    if "name" in data:
        address.name = data["name"]
    if "latitude" in data:
        address.latitude = data["latitude"]
    if "longitude" in data:
        address.longitude = data["longitude"]

    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def delete_address(db: Session, address: Address) -> None:
    db.delete(address)
    db.commit()
