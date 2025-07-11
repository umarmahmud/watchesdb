from fastapi import APIRouter, Depends, HTTPException, Response, status, Security
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated, List
import logging
from datetime import datetime, timezone
from fastapi_cache.decorator import cache

from ..db import get_db
from .model import Manufacturer
from .service import get_all, get_one, create
from ..exceptions import NotFoundError
from ..auth.model import User
from ..auth.auth import get_current_user

router = APIRouter()


@router.get("/manufacturers")
@cache(expire=300)
async def get_all_manufacturers(db_session: Annotated[Session, Depends(get_db)]) -> List[Manufacturer]:
    manufacturers = await get_all(db_session)
    return manufacturers


@router.get("/manufacturers/{manufacturer}")
@cache(expire=300)
async def get_manufacturer(db_session: Annotated[Session, Depends(get_db)], manufacturer: str) -> Manufacturer:
    try:
        m = await get_one(db_session, manufacturer)
        return m
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.post("/manufacturers")
async def create_manufacturer(
    db_session: Annotated[Session, Depends(get_db)],
    manufacturer: Manufacturer,
    response: Response,
    user: User = Security(get_current_user, scopes=["admin"])
) -> Manufacturer:
    try:
        await create(db_session, manufacturer)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=e.args)
    logging.info(f"Created by admin {user.username} at {datetime.now(timezone.utc)}")
    response.status_code = status.HTTP_201_CREATED
    return manufacturer