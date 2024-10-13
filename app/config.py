from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = "postgresql://postgres:password@db:5432/auth_db"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
