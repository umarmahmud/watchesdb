from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated, List

from ..db import get_db
from .model import WatchCreate, Watch
from .service import get_all, get_one, create
from ..exceptions import NotFoundError

router = APIRouter()


@router.get("/watches")
def get_all_watches(db_session: Annotated[Session, Depends(get_db)]) -> List[Watch]:
    watches = get_all(db_session)
    return watches


@router.get("/watches/{id}")
def get_watch(db_session: Annotated[Session, Depends(get_db)], id: int) -> Watch:
    try:
        watch = get_one(db_session, id)
        return watch
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.post("/watches")
def create_watch(db_session: Annotated[Session, Depends(get_db)], watch: WatchCreate) -> WatchCreate:
    try:
        create(db_session, watch)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=e.args)
    return watch
