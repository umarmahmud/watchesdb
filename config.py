import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env = os.getenv("ENV", default="dev").lower()


if env == "prod":
    load_dotenv(".env")
elif env == "test":
    load_dotenv(".env.test")
else:
    load_dotenv(".env.dev")


class Settings(BaseSettings):
    ENV: str = env
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str
    SECRET: str

    class Config:
        case_sensitive = True


settings = Settings()
