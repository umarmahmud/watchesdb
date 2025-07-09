from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import settings

env = settings.ENV
user = settings.POSTGRES_USER
password = settings.POSTGRES_PASSWORD
database = settings.POSTGRES_DATABASE


db_url = f'postgresql+asyncpg://{user}:{password}@db-{env}/{database}'
engine = create_async_engine(db_url, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session