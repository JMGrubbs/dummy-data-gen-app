from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres"
    redis_url: str = "redis://db-cache:6379/0"
    cookie_key: str = "access_token"
    cookie_secure: bool = False
    auth_api_url: str = "https://dauth.johnmgrubbs.io"
    frontend_origin_url: list[str]
    admin_api_key: str | None = None
    reciver_url: str = "http://reciver:8000"
    celery_broker_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
