from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import select

from .model import UserTable, User

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


password_context = CryptContext(schemes="bcrypt", bcrypt__rounds=12)


def find_user(db_session, username: User):
    stmt = select(UserTable).where(UserTable.username == username)
    result = db_session.execute(statement=stmt)
    user = result.scalars().first()
    if user:
        return user
    else:
        return None


def verify_password(password, hashed_password):
    return password_context.verify(password, hashed_password)
    

def authenticate_user(username, password):
    user = find_user(username)
    if not user:
        return "User not found"
    if not verify_password(password, user.pwd):
        return "Not authenticated"
    return user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = find_user(form_data.username)
    if not user:
        return "Incorrect username or password"
    if not verify_password(form_data.username, user.pwd):
        return "Incorrect username or password"

    return {"access_token": user.username, "token_type": "bearer"}