import logging
from sqlalchemy import select, insert, delete, and_

from .model import WatchTable, WatchCreate, FavoriteWatchTable
from ..exceptions import NotFoundError


def get_all(db_session):
    stmt = select(WatchTable)
    result = db_session.execute(stmt)
    return result.scalars().all()


# for any given user, we want manufacturer and model of favorited watches, not rows from 'favorites' table
def get_all_favorites(db_session, username):
    # filter 'favorites' table to get rows for user
    user_favorites = select(FavoriteWatchTable).where(FavoriteWatchTable.username == username).subquery()
    # do an inner join to get favorited watch manufacturer and model information
    stmt = select(WatchTable.manufacturer, WatchTable.model).join(user_favorites, user_favorites.c.watch_id == WatchTable.watch_id)
    results = db_session.execute(stmt).all()
    response = [{"manufacturer": m, "model": mdl} for m, mdl in results]
    return response


def toggle_favorites(db_session, username, favorite):
    stmt = select(FavoriteWatchTable).where(
        and_(FavoriteWatchTable.watch_id == favorite.watch_id,
             FavoriteWatchTable.username == username
        )
    )
    result = db_session.execute(stmt)
    # check to see if watch is already favorited and un-favorite it if it already is favorited
    if result.scalars().first() != None:
        stmt = delete(FavoriteWatchTable).where(
            and_(FavoriteWatchTable.watch_id == favorite.watch_id,
                 FavoriteWatchTable.username == username
            )
        )
        db_session.execute(stmt)
        db_session.commit()
        logging.info(f'The watch with watch_id {favorite.watch_id} un-favorited')
    else:
        stmt = insert(FavoriteWatchTable).values(
            username=username,
            watch_id=favorite.watch_id
        )
        db_session.execute(stmt)
        db_session.commit()
        logging.info(f'The watch with watch_id {favorite.watch_id} favorited')


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
