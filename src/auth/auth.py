from typing import Annotated
from datetime import datetime, timedelta, timezone
import logging

from fastapi import APIRouter, Depends, HTTPException, Response, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError

from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from .model import UserTable, User, Token, UserCreate
from ..db import get_db
from config import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={"standard": "read access", "admin": "write access"}
)

password_context = CryptContext(schemes="bcrypt", bcrypt__rounds=12)

# used for encoding and decoding jwt tokens
secret_key = settings.SECRET
algorithm = "HS256"
token_expire_time = 60

# jwt claims
issuer = ""
audience = ""

router = APIRouter()

async def find_user(db_session, username) -> User:
    stmt = select(UserTable).where(UserTable.username == username)
    result = await db_session.execute(statement=stmt)
    user = result.scalars().first()
    if user:
        return user
    else:
        return None


def verify_password(password, hashed_password):
    return password_context.verify(password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)
    

async def authenticate_user(db_session, username, password) -> User:
    user = await find_user(db_session, username)
    if not user:
        return False
    verified = await run_in_threadpool(verify_password, password, user.password)
    if not verified:
        return False
    return user


def create_token(user: User):
    to_encode = {}
    to_encode.update({"iss": issuer})
    to_encode.update({"aud": audience})
    time_now = datetime.now(timezone.utc)
    expire = time_now + timedelta(minutes=token_expire_time)
    to_encode.update({"iat": time_now})
    to_encode.update({"nbf": time_now})
    to_encode.update({"exp": expire})
    to_encode.update({"sub": user.username})
    if user.is_admin:
        to_encode.update({"scopes": ["admin", "standard"]})
    else:
        to_encode.update({"scopes": ["standard"]})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    logging.info("TOKEN ISSUED")
    return encoded_jwt


async def get_current_user(
    db_session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    security_scopes: SecurityScopes
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username = payload.get("sub")
        token_scopes = payload.get("scopes", [])
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await find_user(db_session, username)
    if user is None:
        raise credentials_exception
    if not any(scope in token_scopes for scope in security_scopes.scopes):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return user


# authenticates user, then creates a token based on supplying the correct username and password
@router.post("/login", response_model=Token)
async def login(db_session: Annotated[Session, Depends(get_db)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(db_session, form_data.username, form_data.password)
    if not user:
        logging.warning(f'FAILED LOGIN ATTEMPT at {datetime.now(timezone.utc)} by {form_data.username}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_token(user=user)
    return Token(access_token=access_token, token_type="Bearer")


@router.post("/signup")
async def sign_up(db_session: Annotated[Session, Depends(get_db)], user: UserCreate, response: Response):
    existing_user = await find_user(db_session, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    username = user.username
    password = await run_in_threadpool(get_password_hash, user.password)
    stmt = insert(UserTable).values(
        username=username,
        password=password,
        is_admin=False
    )
    await db_session.execute(stmt)
    await db_session.commit()
    response.status_code = status.HTTP_201_CREATED
    return { "user": username }