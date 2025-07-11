from fastapi import APIRouter, Depends, HTTPException, Response, status, Security
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated, List
import logging
from datetime import datetime, timezone
from fastapi_cache.decorator import cache

from ..db import get_db
from .model import Movement
from .service import get_all, get_one, create
from ..exceptions import NotFoundError
from ..auth.model import User
from ..auth.auth import get_current_user

router = APIRouter()


@router.get("/movements")
@cache(expire=300)
async def get_all_movements(db_session: Annotated[Session, Depends(get_db)]) -> List[Movement]:
    watches = await get_all(db_session)
    return watches


@router.get("/movements/{movement}")
@cache(expire=300)
async def get_movement(db_session: Annotated[Session, Depends(get_db)], movement: str) -> Movement:
    try:
        m = await get_one(db_session, movement)
        return m
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.post("/movements")
async def create_movement(
    db_session: Annotated[Session, Depends(get_db)],
    movement: Movement,
    response: Response,
    user: User = Security(get_current_user, scopes=["admin"])
) -> Movement:
    try:
        await create(db_session, movement)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=e.args)
    logging.info(f"Created by admin {user.username} at {datetime.now(timezone.utc)}")
    response.status_code = status.HTTP_201_CREATED
    return movement
