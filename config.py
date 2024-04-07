from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    API_VERSION_STR: str = "/api/v1"
    DEBUG: bool = config("DEBUG", default=False, cast=bool)
    MONGO_DB_URL: str = config("MONGO_DB_URL")
    DATABASE: str = "students"
    COLLECTION: str = "students"


settings = Settings()