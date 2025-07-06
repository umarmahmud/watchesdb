from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated, List

from ..db import get_db
from .model import Manufacturer
from .service import get_all, get_one, create
from ..exceptions import NotFoundError

router = APIRouter()


@router.get("/manufacturers")
def get_all_manufacturers(db_session: Annotated[Session, Depends(get_db)]) -> List[Manufacturer]:
    manufacturers = get_all(db_session)
    return manufacturers


@router.get("/manufacturers/{manufacturer}")
def get_manufacturer(db_session: Annotated[Session, Depends(get_db)], manufacturer: str) -> Manufacturer:
    try:
        m = get_one(db_session, manufacturer)
        return m
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args)


@router.post("/manufacturers")
def create_manufacturer(db_session: Annotated[Session, Depends(get_db)], manufacturer: Manufacturer, response: Response) -> Manufacturer:
    try:
        create(db_session, manufacturer)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=e.args)
    response.status_code = status.HTTP_201_CREATED
    return manufacturer