from passlib.context import CryptContext
from sqlalchemy import select

from .model import UserTable, User

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