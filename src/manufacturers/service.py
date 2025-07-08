import logging
from sqlalchemy import select, insert

from .model import ManufacturerTable, Manufacturer
from ..exceptions import NotFoundError


async def get_all(db_session):
    stmt = select(ManufacturerTable)
    result = await db_session.execute(stmt)
    return result.scalars().all()


async def get_one(db_session, manufacturer: str):
    stmt = select(ManufacturerTable).where(ManufacturerTable.manufacturer == manufacturer)
    result = await db_session.execute(stmt)
    m = result.scalars().first()
    if m:
        return m
    else:
        raise NotFoundError({ "message": "manufacturer not found" })


async def create(db_session, manufacturer: Manufacturer):
    stmt = insert(ManufacturerTable).values(
        manufacturer=manufacturer.manufacturer,
        origin=manufacturer.origin,
        established=manufacturer.established,
        luxury=manufacturer.luxury,
    )
    result = await db_session.execute(stmt)
    await db_session.commit()
    logging.info(f'The following manufacturer was inserted: {result.inserted_primary_key[0]}')