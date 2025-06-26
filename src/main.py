from fastapi import FastAPI
from watches.router import router as watch_router
from manufacturers.router import router as manufacturer_router
from movements.router import router as movement_router
from logger import configure_logging

configure_logging()

app = FastAPI()


app.include_router(watch_router)
app.include_router(manufacturer_router)
app.include_router(movement_router)


@app.get("/")
def read_root():
    return { "msg": "Welcome to WatchesDB!" }

