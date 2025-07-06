from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated, List

from ..db import get_db
from .model import WatchCreate, Watch, FavoriteWatch, FavoriteWatchGet
from .service import get_all, get_one, create, get_all_favorites, toggle_favorites
from ..exceptions import NotFoundError
from ..auth.model import User
from ..auth.auth import get_current_user

router = APIRouter()


@router.get("/watches")
def get_all_watches(db_session: Annotated[Session, Depends(get_db)]) -> List[Watch]:
    watches = get_all(db_session)
    return watches


@router.get("/watches/favorites")
def get_favorites(db_session: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]) -> List[FavoriteWatchGet]:
    favorites = get_all_favorites(db_session, user.username)
    return favorites


@router.get("/watches/{id}")
def get_watch(db_session: Annotated[Session, Depends(get_db)], id: int) -> Watch:
    try:
        watch = get_one(db_session, id)
        return watch
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.post("/watches/favorites")
def set_favorites(db_session: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)], favorite: FavoriteWatch, response: Response):
    try:
        toggle_favorites(db_session, user.username, favorite)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=e.args)
    response.status_code = status.HTTP_201_CREATED
    return favorite


@router.post("/watches")
def create_watch(db_session: Annotated[Session, Depends(get_db)], watch: WatchCreate, response: Response) -> WatchCreate:
    try:
        create(db_session, watch)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=e.args)
    response.status_code = status.HTTP_201_CREATED
    return watch
