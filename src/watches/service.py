import logging
from sqlalchemy import select, insert

from .model import WatchTable, WatchCreate
from ..exceptions import NotFoundError


def get_all(db_session):
    stmt = select(WatchTable)
    result = db_session.execute(stmt)
    return result.scalars().all()


def get_one(db_session, id: int):
    stmt = select(WatchTable).where(WatchTable.watch_id == id)
    result = db_session.execute(stmt)
    watch = result.scalars().first()
    if watch:
        return watch
    else:
        raise NotFoundError({ "message": "watch_id not found" })


def create(db_session, watch: WatchCreate):
    stmt = insert(WatchTable).values(
        manufacturer=watch.manufacturer,
        model=watch.model,
        movement=watch.movement,
        case_material=watch.case_material,
        case_diameter=watch.case_diameter,
        dial=watch.dial,
        crystal=watch.crystal,
        bracelet=watch.bracelet,
        strap=watch.strap,
        trending_price=watch.trending_price,
        image_path=watch.image_path
    )
    result = db_session.execute(stmt)
    db_session.commit()
    logging.info(f'The following watch_id was inserted: {result.inserted_primary_key[0]}')
