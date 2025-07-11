from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis

from .watches.router import router as watch_router
from .manufacturers.router import router as manufacturer_router
from .movements.router import router as movement_router
from .auth.auth import router as auth_router
from .logger import configure_logging

configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    
    yield

    await redis_client.close()


app = FastAPI(lifespan=lifespan)


app.include_router(watch_router)
app.include_router(manufacturer_router)
app.include_router(movement_router)
app.include_router(auth_router)


@app.get("/")
async def read_root():
    response = {
        "message": "Welcome to WatchesDB!",
        "version": "1.0.0",
        "description": "This API provides access to watch data including brands, models, movements and trending prices.",
        "documentation_url": "/docs",
        "license_info": {
            "name": "MIT"
        }
    }
    return response