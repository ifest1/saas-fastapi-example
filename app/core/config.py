from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DB_URL: str = Field(..., env="DATABASE_URL")
    API_VERSION: str = "/api/v1"
    JWT_SECRET: str = "blabla"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()
