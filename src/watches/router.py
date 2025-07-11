from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Security
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated, List
import logging
from datetime import datetime, timezone

from ..db import get_db
from .model import WatchCreate, Watch, FavoriteWatch, FavoriteWatchGet, FilterWatchQueryParams
from .service import get_all, get_one, create, get_all_favorites, set_as_favorite, unset_as_favorite, filter_watches
from ..exceptions import NotFoundError, AlreadyExistsError
from ..auth.model import User
from ..auth.auth import get_current_user

router = APIRouter()


@router.get("/watches")
async def get_all_watches(db_session: Annotated[Session, Depends(get_db)]) -> List[Watch]:
    watches = await get_all(db_session)
    return watches


@router.get("/watches/filter")
async def get_filtered_watches(db_session: Annotated[Session, Depends(get_db)], request: Request) -> List[Watch]:
    if not request.query_params:
        raise HTTPException(status_code=422, detail="No query parameters provided.")
    try:
        res = await filter_watches(db_session, request.query_params)
        return res
    except ValidationError:
        raise HTTPException(status_code=422, detail="Extra inputs are not permitted")


@router.get("/watches/favorites")
async def get_favorites(
    db_session: Annotated[Session, Depends(get_db)],
    user: User = Security(get_current_user, scopes=["standard", "admin"])
) -> List[FavoriteWatchGet]:
    favorites = await get_all_favorites(db_session, user.username)
    return favorites


@router.get("/watches/{id}")
async def get_watch(db_session: Annotated[Session, Depends(get_db)], id: int) -> Watch:
    try:
        watch = await get_one(db_session, id)
        return watch
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.post("/watches/favorites")
async def set_favorites(
    db_session: Annotated[Session, Depends(get_db)],
    favorite: FavoriteWatch,
    response: Response,
    user: User = Security(get_current_user, scopes=["standard", "admin"]),
) -> FavoriteWatch:
    try:
        await set_as_favorite(db_session, user.username, favorite)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=e.args)
    except AlreadyExistsError as already_exists_e:
        raise HTTPException(status_code=409, detail=already_exists_e.args)
    response.status_code = status.HTTP_201_CREATED
    return favorite


@router.delete("/watches/favorites")
async def unset_favorites(
    db_session: Annotated[Session, Depends(get_db)],
    favorite: FavoriteWatch,
    response: Response,
    user: User = Security(get_current_user, scopes=["standard", "admin"]),
) -> FavoriteWatch:
    try:
        await unset_as_favorite(db_session, user.username, favorite)
        return favorite
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args)
    except Exception as e:
        raise HTTPException(status_code=500)


@router.post("/watches")
async def create_watch(
    db_session: Annotated[Session, Depends(get_db)],
    watch: WatchCreate,
    response: Response,
    user: User = Security(get_current_user, scopes=["admin"])
) -> WatchCreate:
    try:
        await create(db_session, watch)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=e.args)
    logging.info(f"Created by admin {user.username} at {datetime.now(timezone.utc)}")
    response.status_code = status.HTTP_201_CREATED
    return watch
