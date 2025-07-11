import logging
from sqlalchemy import select, insert, delete, and_
from sqlalchemy.orm import aliased

from .model import WatchTable, WatchCreate, FavoriteWatchTable, FilterWatchQueryParams
from ..exceptions import NotFoundError, AlreadyExistsError


async def get_all(db_session):
    stmt = select(WatchTable)
    result = await db_session.execute(stmt)
    return result.scalars().all()


# filter watches on: manufacturer, case_material, case_diameter, crystal
async def filter_watches(db_session, data):
    data_dict = {k: data.getlist(k) for k in data.keys()}
    params = FilterWatchQueryParams(**data_dict)
    subqueries = []
    if params.manufacturer:
        subqueries.append(select(WatchTable).where(WatchTable.manufacturer.in_(params.manufacturer)).subquery())
    if params.case_material:
        subqueries.append(select(WatchTable).where(WatchTable.case_material.in_(params.case_material)).subquery())
    if params.case_diameter:
        subqueries.append(select(WatchTable).where(WatchTable.case_diameter.in_(params.case_diameter)).subquery())
    if params.crystal:
        subqueries.append(select(WatchTable).where(WatchTable.crystal.in_(params.crystal)).subquery())
    # alias each subquery so we can refer to them separately
    aliases = [aliased(WatchTable, subq) for subq in subqueries]
    # start building the statement from the first alias
    base_alias = aliases[0]
    stmt = select(base_alias)
    # join all remaining aliases on `watch_id`
    for alias in aliases[1:]:
        stmt = stmt.join(alias, alias.watch_id == base_alias.watch_id)
    results = await db_session.execute(stmt)
    return results.scalars().all()


# return only manufacturer and model of favorited watches
async def get_all_favorites(db_session, username):
    # filter 'favorites' table to get rows for user
    user_favorites = select(FavoriteWatchTable).where(FavoriteWatchTable.username == username).subquery()
    # do an inner join to get favorited watch manufacturer and model
    stmt = select(WatchTable.manufacturer, WatchTable.model).join(user_favorites, user_favorites.c.watch_id == WatchTable.watch_id)
    results = await db_session.execute(stmt)
    response = [{"manufacturer": m, "model": mdl} for m, mdl in results.all()]
    return response


async def set_as_favorite(db_session, username, favorite):
    stmt = select(FavoriteWatchTable).where(
        and_(FavoriteWatchTable.watch_id == favorite.watch_id,
             FavoriteWatchTable.username == username
        )
    )
    result = await db_session.execute(stmt)
    if result.scalars().first() is not None:
        raise AlreadyExistsError({ "message": "watch is already in favorites" })
    stmt = insert(FavoriteWatchTable).values(
        username=username,
        watch_id=favorite.watch_id
    )
    await db_session.execute(stmt)
    await db_session.commit()
    logging.info(f'The watch with watch_id {favorite.watch_id} favorited')


async def unset_as_favorite(db_session, username, favorite):
    try:
        stmt = select(FavoriteWatchTable).where(
            and_(FavoriteWatchTable.watch_id == favorite.watch_id,
                FavoriteWatchTable.username == username
            )
        )
        result = await db_session.execute(stmt)
        favorite_to_delete = result.scalars().first()
        if favorite_to_delete is None:
            raise NotFoundError({ "message": "watch to be deleted is not in favorites" })
        await db_session.delete(favorite_to_delete)
        await db_session.commit()
        logging.info(f'The watch with watch_id {favorite.watch_id} un-favorited')
    except NotFoundError as e:
        await db_session.rollback()
        raise e
    except Exception as e:
        await db_session.rollback()
        raise e


async def get_one(db_session, id: int):
    stmt = select(WatchTable).where(WatchTable.watch_id == id)
    result = await db_session.execute(stmt)
    watch = result.scalars().first()
    if watch:
        return watch
    else:
        raise NotFoundError({ "message": "watch_id not found" })


async def create(db_session, watch: WatchCreate):
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
    result = await db_session.execute(stmt)
    await db_session.commit()
    logging.info(f'The following watch_id was inserted: {result.inserted_primary_key[0]}')
