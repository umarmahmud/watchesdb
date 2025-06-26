import logging
from sqlalchemy import select, insert

from .model import MovementTable, Movement
from exceptions import NotFoundError


def get_all(db_session):
    stmt = select(MovementTable)
    result = db_session.execute(stmt)
    return result.scalars().all()


def get_one(db_session, movement: str):
    stmt = select(MovementTable).where(MovementTable.movement == movement)
    result = db_session.execute(stmt)
    m = result.scalars().first()
    if m:
        return m
    else:
        raise NotFoundError({ "message": "movement not found" })


def create(db_session, movement: Movement):
    stmt = insert(MovementTable).values(
        movement=movement.movement,
        movement_type=movement.movement_type,
        jewels=movement.jewels,
        power_reserve=movement.power_reserve,
        manufacturer=movement.manufacturer
    )
    result = db_session.execute(stmt)
    db_session.commit()
    logging.info(f'The following movement was inserted: {result.inserted_primary_key[0]}')