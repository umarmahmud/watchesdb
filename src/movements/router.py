from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated, List

from ..db import get_db
from .model import Movement
from .service import get_all, get_one, create
from ..exceptions import NotFoundError

router = APIRouter()


@router.get("/movements")
def get_all_movements(db_session: Annotated[Session, Depends(get_db)]) -> List[Movement]:
    watches = get_all(db_session)
    return watches


@router.get("/movements/{movement}")
def get_movement(db_session: Annotated[Session, Depends(get_db)], movement: str) -> Movement:
    try:
        m = get_one(db_session, movement)
        return m
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.post("/movements")
def create_movement(db_session: Annotated[Session, Depends(get_db)], movement: Movement) -> Movement:
    try:
        create(db_session, movement)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=e.args)
    return movement
